const reader = document.querySelector("#policy-reader");
const select = document.querySelector("#repo-select");
const readerStatus = document.querySelector("#reader-status");
const policyGrid = document.querySelector("#policy-grid");
const statsStrip = document.querySelector("#stats-strip");

const policyLabels = {
  accepts_external_prs: "External pull requests",
  requires_issue_first: "Issue first",
  ai_assisted_code: "AI assisted code",
  ai_authored_pr_text: "AI written PR text",
};

const stanceLabels = {
  allowed: ["Allowed", "is-open"],
  allowed_with_conditions: ["Conditional", "is-caution"],
  not_stated: ["Not stated", "is-neutral"],
  disallowed: ["Disallowed", "is-stop"],
};

const percentFormat = new Intl.NumberFormat(undefined, {
  style: "percent",
  maximumFractionDigits: 0,
});
const numberFormat = new Intl.NumberFormat(undefined, {
  maximumFractionDigits: 2,
});
const dateFormat = new Intl.DateTimeFormat(undefined, {
  year: "numeric",
  month: "short",
  day: "numeric",
  timeZone: "UTC",
});

function policyValue(entry, claim) {
  if (claim === "accepts_external_prs") {
    return entry.policy[claim] ? ["Accepted", "is-open"] : ["Not accepted", "is-stop"];
  }
  if (claim === "requires_issue_first") {
    return entry.policy[claim] ? ["Required", "is-caution"] : ["Not required", "is-neutral"];
  }
  return stanceLabels[entry.policy[claim]];
}

function evidenceLine(entry, claim) {
  const evidence = entry.evidence[claim];
  if (!evidence) {
    const text = claim === "requires_issue_first"
      ? "No requirement found in files read"
      : "No restriction found in files read";
    return `<small>${text}</small>`;
  }
  return `<a href="${evidence.url}">Read ${evidence.source}</a>`;
}

function formatDays(value) {
  return value === undefined ? "Not available" : `${numberFormat.format(value)} days`;
}

function renderEntry(entry) {
  reader.dataset.repo = entry.repo;
  document.querySelector("#record-repo").textContent = entry.repo;
  const date = document.querySelector("#record-date");
  date.dateTime = entry.measured_at;
  date.textContent = dateFormat.format(new Date(`${entry.measured_at}T00:00:00Z`));

  const claims = Object.keys(policyLabels);
  policyGrid.innerHTML = claims.map((claim, index) => {
    const [label, state] = policyValue(entry, claim);
    return `<div class="policy-item ${state}">
      <span class="policy-index">${String(index + 1).padStart(2, "0")}</span>
      <div><span class="policy-question">${policyLabels[claim]}</span><strong>${label}</strong>${evidenceLine(entry, claim)}</div>
    </div>`;
  }).join("");

  const stats = entry.stats;
  const acceptance = stats.casual_author_acceptance === undefined
    ? "Not available"
    : percentFormat.format(stats.casual_author_acceptance);
  statsStrip.innerHTML = `
    <div><span>CASUAL ACCEPTANCE</span><strong>${acceptance}</strong></div>
    <div><span>MEDIAN TO MERGE</span><strong>${formatDays(stats.median_days_to_merge)}</strong></div>
    <div><span>P90 TO MERGE</span><strong>${formatDays(stats.p90_days_to_merge)}</strong></div>
    <div><span>SAMPLE RECENCY</span><strong>${formatDays(stats.median_close_age_days)}</strong></div>`;

  reader.classList.remove("reader-updated");
  requestAnimationFrame(() => reader.classList.add("reader-updated"));
  readerStatus.textContent = `Showing ${entry.repo}`;
  const url = new URL(location.href);
  url.hash = `repo=${encodeURIComponent(entry.repo)}`;
  history.replaceState(null, "", url);
}

if (reader && select) {
  fetch("repos.json")
    .then((response) => {
      if (!response.ok) throw new Error("Dataset request failed");
      return response.json();
    })
    .then((entries) => {
      if (entries.length === 0) {
        readerStatus.textContent = "No measured projects are available yet.";
        select.disabled = true;
        return;
      }
      const byRepo = new Map(entries.map((entry) => [entry.repo, entry]));
      const hashRepo = decodeURIComponent(location.hash.replace("#repo=", ""));
      const initial = byRepo.has(hashRepo) ? hashRepo : "directus/directus";
      select.value = initial;
      renderEntry(byRepo.get(initial) || entries[0]);
      select.addEventListener("change", () => renderEntry(byRepo.get(select.value)));
    })
    .catch(() => {
      readerStatus.textContent = "The live reader could not load. The static dataset remains available below.";
    });
}

const datasetSearch = document.querySelector("#dataset-search");
const datasetRows = [...document.querySelectorAll("#dataset tbody tr")];
const filterStatus = document.querySelector("#filter-status");

const initialFilter = new URL(location.href).searchParams.get("filter") || "";
if (datasetSearch && initialFilter) {
  datasetSearch.value = initialFilter;
}

function filterDataset() {
  const query = datasetSearch.value.trim().toLowerCase();
  let shown = 0;
  datasetRows.forEach((row) => {
    const visible = row.dataset.repo.includes(query);
    row.hidden = !visible;
    if (visible) shown += 1;
  });
  filterStatus.textContent = `${shown} ${shown === 1 ? "project" : "projects"} shown`;
  const url = new URL(location.href);
  if (query) url.searchParams.set("filter", query);
  else url.searchParams.delete("filter");
  history.replaceState(null, "", url);
}

datasetSearch?.addEventListener("input", filterDataset);
if (initialFilter) filterDataset();

const copyStatus = document.querySelector("#copy-status");
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const original = button.textContent;
    try {
      await navigator.clipboard.writeText(button.dataset.copy);
      button.textContent = "Copied";
      copyStatus.textContent = "Command copied to clipboard";
    } catch {
      button.textContent = "Select text";
      copyStatus.textContent = "Clipboard access failed. Select the command text instead.";
    }
    window.setTimeout(() => {
      button.textContent = original;
    }, 1800);
  });
});
