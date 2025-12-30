import { FormEvent, useMemo, useState } from "react";

const navItems = [
  "Overview",
  "Supply Chain",
  "Services",
  "Policies",
  "Observability",
  "Settings",
];

const highlights = [
  {
    title: "SLSA L3 Provenance",
    value: "100%",
    detail: "All builds attested",
  },
  {
    title: "SBOM Coverage",
    value: "5/5",
    detail: "CycloneDX + SPDX",
  },
  {
    title: "Binary Authorization",
    value: "Active",
    detail: "Prod gate enforced",
  },
  {
    title: "Mean Build Time",
    value: "6m 42s",
    detail: "-12% vs last week",
  },
];

const pipelineSteps = [
  {
    label: "Bazel Build",
    status: "success",
    meta: "98 targets",
  },
  {
    label: "Unit & E2E Tests",
    status: "success",
    meta: "412 passed",
  },
  {
    label: "SBOM Generation",
    status: "success",
    meta: "CycloneDX + SPDX",
  },
  {
    label: "Provenance",
    status: "success",
    meta: "SLSA level 3",
  },
  {
    label: "Cosign + KMS",
    status: "success",
    meta: "Key version 12",
  },
  {
    label: "Binary Authz Gate",
    status: "pending",
    meta: "2 pending",
  },
];

const services = [
  {
    name: "users",
    language: "Go",
    endpoint: "/v1/users",
    status: "healthy",
    latency: "84ms",
    owner: "platform@",
  },
  {
    name: "orders",
    language: "Python",
    endpoint: "/v1/orders",
    status: "healthy",
    latency: "122ms",
    owner: "commerce@",
  },
  {
    name: "inventory",
    language: "Java",
    endpoint: "/v1/inventory",
    status: "warning",
    latency: "221ms",
    owner: "ops@",
  },
  {
    name: "payments",
    language: "Node",
    endpoint: "/v1/payments",
    status: "healthy",
    latency: "98ms",
    owner: "finance@",
  },
  {
    name: "notifications",
    language: "Rust",
    endpoint: "/v1/notifications",
    status: "healthy",
    latency: "67ms",
    owner: "growth@",
  },
];

const sboms = [
  {
    name: "users",
    format: "CycloneDX",
    updated: "2 mins ago",
    deps: "42",
  },
  {
    name: "orders",
    format: "SPDX",
    updated: "6 mins ago",
    deps: "58",
  },
  {
    name: "inventory",
    format: "CycloneDX",
    updated: "10 mins ago",
    deps: "63",
  },
  {
    name: "payments",
    format: "SPDX",
    updated: "12 mins ago",
    deps: "31",
  },
  {
    name: "notifications",
    format: "CycloneDX",
    updated: "14 mins ago",
    deps: "26",
  },
];

const policies = [
  {
    title: "Disallow :latest",
    description: "Block mutable tags in all namespaces.",
    status: "enforced",
  },
  {
    title: "Required resource limits",
    description: "Ensure CPU and memory requests/limits.",
    status: "enforced",
  },
  {
    title: "Signed images only",
    description: "Cosign + KMS signature required.",
    status: "enforced",
  },
  {
    title: "Provenance annotation",
    description: "SLSA provenance reference required.",
    status: "advisory",
  },
];

const incidents = [
  {
    title: "Inventory service latency",
    time: "12:42 UTC",
    summary: "GC pause detected on inventory pods.",
    status: "investigating",
  },
  {
    title: "Binauthz violation",
    time: "11:18 UTC",
    summary: "Unsigned image blocked in dev namespace.",
    status: "resolved",
  },
  {
    title: "OPA policy update",
    time: "09:50 UTC",
    summary: "Added required labels constraint.",
    status: "completed",
  },
];

const traces = [
  {
    name: "Checkout pipeline",
    duration: "1.8s",
    spans: "42",
    errorRate: "0.4%",
  },
  {
    name: "User signup",
    duration: "620ms",
    spans: "28",
    errorRate: "0.1%",
  },
  {
    name: "Inventory reservation",
    duration: "2.4s",
    spans: "57",
    errorRate: "1.8%",
  },
];

const quickActions = [
  "Trigger demo flow",
  "Generate SBOMs",
  "Verify attestations",
  "Open GUAC graph",
];

const activityFeed = [
  {
    title: "Attested build created",
    detail: "orders-service build #458 signed with KMS.",
    time: "2m ago",
  },
  {
    title: "SBOM ingested",
    detail: "inventory-service CycloneDX uploaded to GUAC.",
    time: "8m ago",
  },
  {
    title: "Policy drift detected",
    detail: "New container missing owner label.",
    time: "12m ago",
  },
  {
    title: "Deployment approved",
    detail: "users-service promoted to prod.",
    time: "28m ago",
  },
];

const environments = [
  {
    name: "dev",
    region: "us-central1",
    gate: "warn",
    builds: "24",
  },
  {
    name: "staging",
    region: "us-east1",
    gate: "enforced",
    builds: "12",
  },
  {
    name: "prod",
    region: "europe-west1",
    gate: "enforced",
    builds: "6",
  },
];

const complianceChecks = [
  {
    label: "SLSA provenance",
    value: 92,
  },
  {
    label: "SBOM completeness",
    value: 88,
  },
  {
    label: "Policy compliance",
    value: 96,
  },
  {
    label: "Artifact signing",
    value: 100,
  },
];

function StatusPill({ status }: { status: string }) {
  return (
    <span className={`pill pill-${status}`}>{status}</span>
  );
}

function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="section-title">
      <div>
        <h2>{title}</h2>
        {subtitle && <p>{subtitle}</p>}
      </div>
      <button className="ghost-button">View all</button>
    </div>
  );
}

export default function App() {
  const [active, setActive] = useState(navItems[0]);
  const [email, setEmail] = useState("");
  const [requested, setRequested] = useState(false);

  const filteredNav = useMemo(() => navItems, []);

  const submit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!email) return;
    setRequested(true);
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="logo">
          <svg viewBox="0 0 40 40" aria-hidden="true">
            <rect x="4" y="4" width="32" height="32" rx="10" />
            <path d="M14 24l5-8 4 6 5-10" />
          </svg>
          <div>
            <h1>SLSA Nexus</h1>
            <span>Supply chain cockpit</span>
          </div>
        </div>
        <nav>
          {filteredNav.map((item) => (
            <button
              key={item}
              className={`nav-item ${active === item ? "active" : ""}`}
              onClick={() => setActive(item)}
              type="button"
            >
              <span>{item}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-card">
          <h3>Next action</h3>
          <p>Upgrade to continuous verification checks.</p>
          <button className="primary">Enable now</button>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h2>{active}</h2>
            <p>Secure software supply chain visibility in one place.</p>
          </div>
          <div className="topbar-actions">
            <button className="ghost-button">Export report</button>
            <button className="primary">Launch demo</button>
          </div>
        </header>

        {active === "Overview" && (
          <div className="page">
            <section className="hero">
              <div>
                <h1>Ship verified software with confidence.</h1>
                <p>
                  Track every build, attestation, and policy gate from source to
                  GKE. Stay audit-ready with live provenance, SBOM, and
                  deployment insights.
                </p>
                <div className="hero-actions">
                  {quickActions.map((action) => (
                    <button key={action} className="chip" type="button">
                      {action}
                    </button>
                  ))}
                </div>
                <div className="trust-row">
                  <div>
                    <span>GUAC graph</span>
                    <strong>1,284 nodes</strong>
                  </div>
                  <div>
                    <span>Attestors</span>
                    <strong>4 active</strong>
                  </div>
                  <div>
                    <span>Registry</span>
                    <strong>Artifact Registry</strong>
                  </div>
                </div>
              </div>
              <div className="hero-graphic">
                <svg viewBox="0 0 420 300" aria-hidden="true">
                  <rect x="18" y="24" width="140" height="90" rx="16" />
                  <rect x="190" y="24" width="210" height="60" rx="16" />
                  <rect x="190" y="98" width="210" height="60" rx="16" />
                  <rect x="18" y="138" width="140" height="110" rx="16" />
                  <circle cx="80" cy="68" r="22" />
                  <path d="M50 198h76M50 218h90" />
                  <path d="M220 54h150M220 78h120" />
                  <path d="M220 128h150M220 152h120" />
                  <path d="M150 80h40M150 180h40" />
                </svg>
                <div className="floating-card">
                  <p>Binary Authz</p>
                  <strong>Gate enforced</strong>
                  <span>2 pending approvals</span>
                </div>
              </div>
            </section>

            <section className="stat-grid">
              {highlights.map((item) => (
                <div key={item.title} className="stat-card">
                  <p>{item.title}</p>
                  <h3>{item.value}</h3>
                  <span>{item.detail}</span>
                </div>
              ))}
            </section>

            <section className="grid two-column">
              <div className="card">
                <SectionTitle
                  title="Supply chain pipeline"
                  subtitle="Latest build: build-all #992"
                />
                <div className="pipeline">
                  {pipelineSteps.map((step) => (
                    <div key={step.label} className="pipeline-step">
                      <div className={`dot dot-${step.status}`} />
                      <div>
                        <strong>{step.label}</strong>
                        <span>{step.meta}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <div className="card">
                <SectionTitle
                  title="Active environments"
                  subtitle="Policy gates by environment"
                />
                <div className="env-list">
                  {environments.map((env) => (
                    <div key={env.name} className="env-item">
                      <div>
                        <strong>{env.name.toUpperCase()}</strong>
                        <span>{env.region}</span>
                      </div>
                      <div className="env-meta">
                        <StatusPill status={env.gate} />
                        <span>{env.builds} builds</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </section>

            <section className="grid three-column">
              {complianceChecks.map((check) => (
                <div key={check.label} className="card">
                  <div className="progress">
                    <div className="progress-label">
                      <strong>{check.label}</strong>
                      <span>{check.value}%</span>
                    </div>
                    <div className="progress-bar">
                      <div
                        className="progress-fill"
                        style={{ width: `${check.value}%` }}
                      />
                    </div>
                  </div>
                </div>
              ))}
            </section>

            <section className="grid two-column">
              <div className="card">
                <SectionTitle
                  title="Recent activity"
                  subtitle="Attestations and policy events"
                />
                <div className="activity">
                  {activityFeed.map((item) => (
                    <div key={item.title} className="activity-item">
                      <div>
                        <strong>{item.title}</strong>
                        <p>{item.detail}</p>
                      </div>
                      <span>{item.time}</span>
                    </div>
                  ))}
                </div>
              </div>
              <div className="card">
                <SectionTitle
                  title="Demo onboarding"
                  subtitle="Invite a teammate to the workspace"
                />
                <form className="invite-form" onSubmit={submit}>
                  <label htmlFor="email">Teammate email</label>
                  <input
                    id="email"
                    type="email"
                    placeholder="devops@example.com"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    required
                  />
                  <button className="primary" type="submit">
                    Send invite
                  </button>
                  {requested && (
                    <p className="success">Invite queued for {email}</p>
                  )}
                </form>
              </div>
            </section>
          </div>
        )}

        {active === "Supply Chain" && (
          <div className="page">
            <section className="grid two-column">
              <div className="card">
                <SectionTitle
                  title="SBOM registry"
                  subtitle="Latest bill of materials uploads"
                />
                <div className="table">
                  {sboms.map((sbom) => (
                    <div key={sbom.name} className="table-row">
                      <div>
                        <strong>{sbom.name}</strong>
                        <span>{sbom.format}</span>
                      </div>
                      <div>
                        <span>{sbom.deps} deps</span>
                      </div>
                      <div>
                        <span>{sbom.updated}</span>
                      </div>
                      <button className="ghost-button" type="button">
                        View
                      </button>
                    </div>
                  ))}
                </div>
              </div>
              <div className="card">
                <SectionTitle
                  title="Attestation ledger"
                  subtitle="in-toto layout + provenance"
                />
                <div className="ledger">
                  <div>
                    <h3>Build provenance</h3>
                    <p>
                      Signed by <strong>Cloud KMS</strong> with identity
                      <code>projects/demo/locations/us/keyRings/supply</code>.
                    </p>
                  </div>
                  <div className="ledger-grid">
                    <div>
                      <span>Predicate type</span>
                      <strong>SLSA v1.0</strong>
                    </div>
                    <div>
                      <span>Builder</span>
                      <strong>cloud-build@</strong>
                    </div>
                    <div>
                      <span>Materials</span>
                      <strong>302 digests</strong>
                    </div>
                    <div>
                      <span>Subjects</span>
                      <strong>5 images</strong>
                    </div>
                  </div>
                  <button className="primary" type="button">
                    Download provenance
                  </button>
                </div>
              </div>
            </section>

            <section className="grid three-column">
              <div className="card">
                <h3>GUAC graph</h3>
                <p>Trace component lineage across repositories.</p>
                <div className="svg-frame">
                  <svg viewBox="0 0 160 120" aria-hidden="true">
                    <circle cx="28" cy="26" r="12" />
                    <circle cx="88" cy="24" r="12" />
                    <circle cx="132" cy="56" r="12" />
                    <circle cx="50" cy="90" r="12" />
                    <circle cx="108" cy="92" r="12" />
                    <path d="M38 28h38M98 30l28 18M32 38l14 44M94 38l12 42" />
                    <path d="M62 90h34" />
                  </svg>
                </div>
              </div>
              <div className="card">
                <h3>Risk scoring</h3>
                <p>Automated CVE + policy risk summary.</p>
                <div className="risk-meter">
                  <span>Low</span>
                  <div className="risk-bar">
                    <div className="risk-fill" />
                  </div>
                  <span>High</span>
                </div>
                <strong className="risk-score">19 / 100</strong>
              </div>
              <div className="card">
                <h3>Attestor coverage</h3>
                <p>Verify required attestations are present.</p>
                <ul className="checklist">
                  <li>✅ Build provenance</li>
                  <li>✅ SBOM attestation</li>
                  <li>✅ Vulnerability scan</li>
                  <li>✅ Policy evaluation</li>
                </ul>
              </div>
            </section>
          </div>
        )}

        {active === "Services" && (
          <div className="page">
            <section className="card">
              <SectionTitle
                title="Microservice health"
                subtitle="Polyglot runtime status"
              />
              <div className="table">
                {services.map((service) => (
                  <div key={service.name} className="table-row">
                    <div>
                      <strong>{service.name}</strong>
                      <span>{service.language}</span>
                    </div>
                    <div>
                      <span>{service.endpoint}</span>
                    </div>
                    <div>
                      <span>{service.latency}</span>
                    </div>
                    <div>
                      <StatusPill status={service.status} />
                    </div>
                    <div>
                      <span>{service.owner}</span>
                    </div>
                    <button className="ghost-button" type="button">
                      Inspect
                    </button>
                  </div>
                ))}
              </div>
            </section>

            <section className="grid two-column">
              <div className="card">
                <SectionTitle
                  title="Release readiness"
                  subtitle="Blocking issues before promotion"
                />
                <div className="callouts">
                  <div className="callout">
                    <h4>Inventory latency spike</h4>
                    <p>Investigate JVM GC pause in staging.</p>
                    <span className="tag">needs attention</span>
                  </div>
                  <div className="callout">
                    <h4>Orders canary ready</h4>
                    <p>Promote to prod after CVE scan completes.</p>
                    <span className="tag success">ready soon</span>
                  </div>
                </div>
              </div>
              <div className="card">
                <SectionTitle
                  title="Service topology"
                  subtitle="Gateway routing map"
                />
                <div className="svg-frame">
                  <svg viewBox="0 0 240 160" aria-hidden="true">
                    <rect x="20" y="20" width="80" height="40" rx="10" />
                    <rect x="140" y="20" width="80" height="40" rx="10" />
                    <rect x="20" y="100" width="80" height="40" rx="10" />
                    <rect x="140" y="100" width="80" height="40" rx="10" />
                    <circle cx="120" cy="80" r="24" />
                    <path d="M100 40h40M100 120h40M60 60v40M180 60v40" />
                  </svg>
                </div>
              </div>
            </section>
          </div>
        )}

        {active === "Policies" && (
          <div className="page">
            <section className="grid two-column">
              {policies.map((policy) => (
                <div key={policy.title} className="card">
                  <div className="policy-card">
                    <div>
                      <h3>{policy.title}</h3>
                      <p>{policy.description}</p>
                    </div>
                    <StatusPill status={policy.status} />
                  </div>
                  <div className="policy-actions">
                    <button className="ghost-button" type="button">
                      View policy
                    </button>
                    <button className="primary" type="button">
                      Update
                    </button>
                  </div>
                </div>
              ))}
            </section>
            <section className="card">
              <SectionTitle
                title="Policy timeline"
                subtitle="Admission control events"
              />
              <div className="timeline">
                {incidents.map((incident) => (
                  <div key={incident.title} className="timeline-item">
                    <div className="timeline-dot" />
                    <div>
                      <strong>{incident.title}</strong>
                      <p>{incident.summary}</p>
                    </div>
                    <div className="timeline-meta">
                      <StatusPill status={incident.status} />
                      <span>{incident.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}

        {active === "Observability" && (
          <div className="page">
            <section className="grid three-column">
              <div className="card">
                <h3>Service latency</h3>
                <p>95th percentile response time.</p>
                <div className="sparkline">
                  <span>92ms</span>
                  <div className="sparkline-bar" />
                </div>
              </div>
              <div className="card">
                <h3>Error budget</h3>
                <p>Remaining budget this month.</p>
                <div className="sparkline">
                  <span>94%</span>
                  <div className="sparkline-bar" />
                </div>
              </div>
              <div className="card">
                <h3>OTel coverage</h3>
                <p>Spans recorded per minute.</p>
                <div className="sparkline">
                  <span>18k</span>
                  <div className="sparkline-bar" />
                </div>
              </div>
            </section>

            <section className="card">
              <SectionTitle
                title="Distributed traces"
                subtitle="Critical path performance"
              />
              <div className="table">
                {traces.map((trace) => (
                  <div key={trace.name} className="table-row">
                    <div>
                      <strong>{trace.name}</strong>
                      <span>{trace.spans} spans</span>
                    </div>
                    <div>
                      <span>{trace.duration}</span>
                    </div>
                    <div>
                      <span>{trace.errorRate} errors</span>
                    </div>
                    <button className="ghost-button" type="button">
                      View trace
                    </button>
                  </div>
                ))}
              </div>
            </section>
          </div>
        )}

        {active === "Settings" && (
          <div className="page">
            <section className="grid two-column">
              <div className="card">
                <SectionTitle
                  title="Workspace settings"
                  subtitle="Identity, security, and integrations"
                />
                <div className="settings">
                  <div>
                    <strong>Identity provider</strong>
                    <span>Workload Identity Federation</span>
                  </div>
                  <div>
                    <strong>Key management</strong>
                    <span>Cloud KMS key ring: supply-chain</span>
                  </div>
                  <div>
                    <strong>Artifact registry</strong>
                    <span>us-central1-docker.pkg.dev/demo</span>
                  </div>
                  <div>
                    <strong>Alerting</strong>
                    <span>Slack #supply-chain-alerts</span>
                  </div>
                </div>
              </div>
              <div className="card">
                <SectionTitle
                  title="Security posture"
                  subtitle="Recommended actions"
                />
                <div className="callouts">
                  <div className="callout">
                    <h4>Rotate attestor key</h4>
                    <p>Next rotation window in 14 days.</p>
                    <span className="tag">scheduled</span>
                  </div>
                  <div className="callout">
                    <h4>Enable workload identity</h4>
                    <p>2 services still using static keys.</p>
                    <span className="tag warning">action required</span>
                  </div>
                </div>
              </div>
            </section>
          </div>
        )}
      </main>
    </div>
  );
}
