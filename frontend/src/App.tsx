import { startTransition, useDeferredValue, useEffect, useState } from "react";

type RepoSummary = {
    id: string;
    name: string;
    team: string;
    risk: string;
    health: number;
    openPrs: number;
    securityAlerts: number;
    releaseReady: boolean;
    summary: string;
};

type Dashboard = {
    overview: {
        repos: number;
        avgHealth: number;
        openPrs: number;
        securityAlerts: number;
    };
    repos: RepoSummary[];
    defaultRepoId: string;
};

type RepoDetail = {
    id: string;
    name: string;
    team: string;
    risk: string;
    health: number;
    releaseChannel: string;
    lead: string;
    summary: string;
    signals: { label: string; value: string; trend: string }[];
    checks: { name: string; status: string; detail: string }[];
    pullRequests: { id: number; title: string; owner: string; risk: string; status: string }[];
    alerts: { severity: string; title: string; detail: string }[];
    releaseReadiness: { label: string; status: string }[];
    actions: string[];
};

type ReleasePacket = {
    repoId: string;
    repoName: string;
    risk: string;
    releaseChannel: string;
    summary: string;
    blockedItems: string[];
    reviewItems: string[];
    doneItems: string[];
    recommendedActions: string[];
    securityAlertCount: number;
    pullRequestCount: number;
};

type RiskExport = {
    repoId: string;
    repoName: string;
    lead: string;
    releaseChannel: string;
    risk: string;
    executiveSummary: string;
    checks: { name: string; status: string; detail: string }[];
    actions: string[];
};

const riskOptions = ["all", "high", "review", "low"];

const App = () => {
    const [dashboard, setDashboard] = useState<Dashboard | null>(null);
    const [detail, setDetail] = useState<RepoDetail | null>(null);
    const [releasePacket, setReleasePacket] = useState<ReleasePacket | null>(null);
    const [riskExport, setRiskExport] = useState<RiskExport | null>(null);
    const [selectedRepoId, setSelectedRepoId] = useState("");
    const [riskFilter, setRiskFilter] = useState("all");
    const [search, setSearch] = useState("");
    const [error, setError] = useState("");
    const deferredSearch = useDeferredValue(search);

    useEffect(() => {
        fetch("/api/repos")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load dashboard");
                }

                return response.json();
            })
            .then((payload: Dashboard) => {
                setDashboard(payload);
                setSelectedRepoId(payload.defaultRepoId);
            })
            .catch(() =>
                setError("Repo Flight Deck could not be loaded. Start the backend and try again.")
            );
    }, []);

    useEffect(() => {
        if (!selectedRepoId) {
            return;
        }

        Promise.all([
            fetch(`/api/repos/${selectedRepoId}`).then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load repo detail");
                }

                return response.json();
            }),
            fetch(`/api/repos/${selectedRepoId}/release-packet`).then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load release packet");
                }

                return response.json();
            }),
            fetch(`/api/repos/${selectedRepoId}/risk-export`).then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load risk export");
                }

                return response.json();
            }),
        ])
            .then(([detailPayload, releasePayload, exportPayload]) => {
                startTransition(() => {
                    setDetail(detailPayload as RepoDetail);
                    setReleasePacket(releasePayload as ReleasePacket);
                    setRiskExport(exportPayload as RiskExport);
                });
            })
            .catch(() =>
                setError("Repo detail could not be loaded. Refresh and try again.")
            );
    }, [selectedRepoId]);

    if (error) {
        return <main className="app-shell status-screen">{error}</main>;
    }

    if (!dashboard || !detail || !releasePacket || !riskExport) {
        return <main className="app-shell status-screen">Loading repo control center...</main>;
    }

    const filteredRepos = dashboard.repos.filter((repo) => {
        const matchesRisk = riskFilter === "all" ? true : repo.risk === riskFilter;
        const haystack = `${repo.name} ${repo.team} ${repo.summary}`.toLowerCase();
        const matchesSearch = haystack.includes(deferredSearch.trim().toLowerCase());
        return matchesRisk && matchesSearch;
    });

    const downloadRiskExport = () => {
        const blob = new Blob([JSON.stringify(riskExport, null, 2)], {
            type: "application/json",
        });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");
        link.href = url;
        link.download = `${riskExport.repoName}-risk-export.json`;
        link.click();
        URL.revokeObjectURL(url);
    };

    return (
        <main className="app-shell">
            <section className="hero">
                <div>
                    <p className="eyebrow">Repo Flight Deck</p>
                    <h1>See which repos are safe to ship and which ones need air traffic control.</h1>
                    <p className="hero-copy">
                        A developer-platform dashboard for repository health, pull request
                        load, CI stability, security work, and release readiness.
                    </p>
                    <div className="hero-tags">
                        <span>CI health</span>
                        <span>PR risk</span>
                        <span>Release gate</span>
                    </div>
                </div>
                <div className="hero-panel">
                    <span>Selected repo</span>
                    <strong>{detail.name}</strong>
                    <p>{detail.summary}</p>
                    <div className="hero-panel__meta">
                        <span>{detail.team}</span>
                        <span>{detail.releaseChannel}</span>
                        <span>Lead: {detail.lead}</span>
                    </div>
                </div>
            </section>

            <section className="metric-grid">
                <article className="metric-card">
                    <span>Repos tracked</span>
                    <strong>{dashboard.overview.repos}</strong>
                </article>
                <article className="metric-card">
                    <span>Average health</span>
                    <strong>{dashboard.overview.avgHealth}</strong>
                </article>
                <article className="metric-card">
                    <span>Open PRs</span>
                    <strong>{dashboard.overview.openPrs}</strong>
                </article>
                <article className="metric-card">
                    <span>Security alerts</span>
                    <strong>{dashboard.overview.securityAlerts}</strong>
                </article>
            </section>

            <section className="content-grid">
                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Repo catalog</p>
                        <h2>What needs attention</h2>
                    </div>
                    <div className="catalog-controls">
                        <label className="control">
                            <span>Search</span>
                            <input
                                type="search"
                                placeholder="mission-console, platform, data-platform..."
                                value={search}
                                onChange={(event) => setSearch(event.target.value)}
                            />
                        </label>
                        <label className="control">
                            <span>Risk</span>
                            <select
                                value={riskFilter}
                                onChange={(event) => setRiskFilter(event.target.value)}
                            >
                                {riskOptions.map((option) => (
                                    <option key={option} value={option}>
                                        {option === "all"
                                            ? "All risks"
                                            : option.charAt(0).toUpperCase() +
                                              option.slice(1)}
                                    </option>
                                ))}
                            </select>
                        </label>
                    </div>
                    <div className="repo-list">
                        {filteredRepos.map((repo) => (
                            <button
                                key={repo.id}
                                className={`repo-card${repo.id === detail.id ? " is-active" : ""}`}
                                onClick={() => setSelectedRepoId(repo.id)}
                                type="button"
                            >
                                <div className="repo-card__top">
                                    <div>
                                        <strong>{repo.name}</strong>
                                        <span>{repo.team}</span>
                                    </div>
                                    <span className={`badge badge--${repo.risk}`}>
                                        {repo.risk}
                                    </span>
                                </div>
                                <p>{repo.summary}</p>
                                <div className="repo-card__meta">
                                    <span>health {repo.health}</span>
                                    <span>{repo.openPrs} PRs</span>
                                    <span>{repo.securityAlerts} alerts</span>
                                    <span>{repo.releaseReady ? "ready" : "not ready"}</span>
                                </div>
                            </button>
                        ))}
                    </div>
                </article>

                <article className="panel">
                    <div className="panel-heading panel-heading--split">
                        <div>
                            <p className="eyebrow">Release packet</p>
                            <h2>{detail.name}</h2>
                        </div>
                        <button className="export-button" onClick={downloadRiskExport} type="button">
                            Export risk packet
                        </button>
                    </div>
                    <div className="comparison-strip">
                        <div className="comparison-card">
                            <span>Risk</span>
                            <strong>{releasePacket.risk}</strong>
                        </div>
                        <div className="comparison-card">
                            <span>Channel</span>
                            <strong>{releasePacket.releaseChannel}</strong>
                        </div>
                        <div className="comparison-card">
                            <span>Security alerts</span>
                            <strong>{releasePacket.securityAlertCount}</strong>
                        </div>
                    </div>
                    <p className="hero-copy">{riskExport.executiveSummary}</p>
                    <div className="signal-grid">
                        {detail.signals.map((signal) => (
                            <div className="signal-card" key={signal.label}>
                                <span>{signal.label}</span>
                                <strong>{signal.value}</strong>
                                <em className={`trend trend--${signal.trend}`}>
                                    {signal.trend}
                                </em>
                            </div>
                        ))}
                    </div>
                </article>
            </section>

            <section className="content-grid">
                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Checks</p>
                        <h2>CI and release status</h2>
                    </div>
                    <div className="stack-list">
                        {detail.checks.map((check) => (
                            <div className="stack-card" key={check.name}>
                                <div className="repo-card__top">
                                    <strong>{check.name}</strong>
                                    <span className={`badge badge--${check.status}`}>
                                        {check.status}
                                    </span>
                                </div>
                                <p>{check.detail}</p>
                            </div>
                        ))}
                    </div>
                </article>

                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Pull requests</p>
                        <h2>Merge queue</h2>
                    </div>
                    <div className="stack-list">
                        {detail.pullRequests.map((pr) => (
                            <div className="stack-card" key={pr.id}>
                                <div className="repo-card__top">
                                    <div>
                                        <strong>#{pr.id} {pr.title}</strong>
                                        <span>{pr.owner}</span>
                                    </div>
                                    <span className={`badge badge--${pr.risk}`}>
                                        {pr.risk}
                                    </span>
                                </div>
                                <p>{pr.status}</p>
                            </div>
                        ))}
                    </div>
                </article>
            </section>

            <section className="content-grid content-grid--bottom">
                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Security</p>
                        <h2>Alert queue</h2>
                    </div>
                    <div className="stack-list">
                        {detail.alerts.map((alert) => (
                            <div className="stack-card" key={alert.title}>
                                <div className="repo-card__top">
                                    <strong>{alert.title}</strong>
                                    <span className={`badge badge--${alert.severity}`}>
                                        {alert.severity}
                                    </span>
                                </div>
                                <p>{alert.detail}</p>
                            </div>
                        ))}
                    </div>
                </article>

                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Release gate</p>
                        <h2>Readiness checklist</h2>
                    </div>
                    <div className="stack-list">
                        {detail.releaseReadiness.map((item) => (
                            <div className="stack-card stack-card--row" key={item.label}>
                                <strong>{item.label}</strong>
                                <span className={`badge badge--${item.status}`}>
                                    {item.status}
                                </span>
                            </div>
                        ))}
                    </div>
                </article>

                <article className="panel">
                    <div className="panel-heading">
                        <p className="eyebrow">Recommended actions</p>
                        <h2>Next steps</h2>
                    </div>
                    <ul className="simple-list simple-list--stacked">
                        {releasePacket.recommendedActions.map((action) => (
                            <li key={action}>{action}</li>
                        ))}
                    </ul>
                </article>
            </section>
        </main>
    );
};

export default App;
