'use client'

import { useMemo, useState, useEffect, useCallback } from 'react'
import { useRouter, usePathname } from 'next/navigation'
import {
  Activity, ArrowUpRight, Bell, Bot, Building2, CalendarDays, Check, ChevronDown, ChevronRight,
  CircleAlert, Clock3, Database, Filter, FolderKanban, Globe, Headphones, Info, LayoutDashboard, Menu,
  MessageSquare, MoreHorizontal, Phone, Plus, RotateCcw, Save, Search, Send, Settings2, ShieldAlert, ShieldCheck, Sparkles,
  Target, UserPlus, UserRound, Users, X, Zap,
} from 'lucide-react'

export const nav = [
  { id: 'dashboard', label: 'Orchestrator', icon: LayoutDashboard },
  { id: 'contacts', label: 'Contact Finding', icon: Target },
  { id: 'outreach', label: 'Outreach Agent', icon: Phone },
  { id: 'followup', label: 'Follow-Up Agent', icon: CalendarDays },
  { id: 'closing', label: 'Closing Agent', icon: ShieldCheck },
  { id: 'pipeline', label: 'Lead Pipeline', icon: FolderKanban },
  { id: 'escalations', label: 'Escalation Inbox', icon: CircleAlert },
  { id: 'database', label: 'Contact Database', icon: Database },
]

export const contacts = [
  { name: 'Maya Chen', role: 'VP of Revenue', company: 'Northstar Labs', location: 'Austin, TX', score: 96, initials: 'MC', tone: 'gold' },
  { name: 'Marcus Bell', role: 'Founder & CEO', company: 'Harbor Systems', location: 'New York, NY', score: 92, initials: 'MB', tone: 'blue' },
  { name: 'Elena Rossi', role: 'Head of Growth', company: 'Verity Health', location: 'San Francisco, CA', score: 89, initials: 'ER', tone: 'coral' },
  { name: 'Theo Adams', role: 'CRO', company: 'Latticeworks', location: 'Chicago, IL', score: 86, initials: 'TA', tone: 'green' },
  { name: 'Nina Patel', role: 'Director of Sales', company: 'Orbit Commerce', location: 'Boston, MA', score: 84, initials: 'NP', tone: 'lavender' },
  { name: 'Jon Bellamy', role: 'VP Partnerships', company: 'Clearpath AI', location: 'Denver, CO', score: 81, initials: 'JB', tone: 'gold' },
]

export const leads = [
  { name: 'Maya Chen', company: 'Northstar Labs', stage: 'Closing', initials: 'MC', value: '$48,000', tone: 'gold' },
  { name: 'Marcus Bell', company: 'Harbor Systems', stage: 'Following Up', initials: 'MB', value: '$32,500', tone: 'blue' },
  { name: 'Elena Rossi', company: 'Verity Health', stage: 'Contacted', initials: 'ER', value: '$18,200', tone: 'coral' },
  { name: 'Theo Adams', company: 'Latticeworks', stage: 'Found', initials: 'TA', value: '$64,000', tone: 'green' },
  { name: 'Nina Patel', company: 'Orbit Commerce', stage: 'Won', initials: 'NP', value: '$26,000', tone: 'lavender' },
  { name: 'Jon Bellamy', company: 'Clearpath AI', stage: 'Lost', initials: 'JB', value: '$12,800', tone: 'gold' },
]

export function Avatar({ initials, tone = 'gold', small = false }: { initials: string; tone?: string; small?: boolean }) {
  return <span className={`avatar avatar-${tone} ${small ? 'avatar-small' : ''}`}>{initials}</span>
}

export function Pill({ children, tone = 'blue' }: { children: React.ReactNode; tone?: string }) {
  return <span className={`pill pill-${tone}`}>{children}</span>
}

export function Glass({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <section className={`glass ${className}`}>{children}</section>
}

export function Sidebar({ active, onSelect }: { active: string; onSelect: (id: string) => void }) {
  return (
    <aside className="sidebar">
      <div className="brand" onClick={() => onSelect('dashboard')} style={{ cursor: 'pointer' }}>
        <span className="brand-mark"><Sparkles size={15} /></span>
        <span>sale<strong>goodman</strong></span>
      </div>
      <div className="workspace">
        <div className="workspace-avatar">S</div>
        <div><small>Workspace</small><b>Goodman & Co.</b></div>
        <ChevronDown size={14} />
      </div>
      <p className="nav-label">AUTOMATION</p>
      <nav>
        {nav.slice(0, 5).map(item => {
          const Icon = item.icon
          return (
            <button
              key={item.id}
              className={active === item.id ? 'nav-item active' : 'nav-item'}
              onClick={() => onSelect(item.id)}
            >
              <Icon size={17} />
              <span>{item.label}</span>
              {item.id === 'dashboard' && <span className="live-dot" />}
            </button>
          )
        })}
      </nav>
      <p className="nav-label nav-label-lower">WORKSPACE</p>
      <nav>
        {nav.slice(5).map(item => {
          const Icon = item.icon
          return (
            <button
              key={item.id}
              className={active === item.id ? 'nav-item active' : 'nav-item'}
              onClick={() => onSelect(item.id)}
            >
              <Icon size={17} />
              <span>{item.label}</span>
              {item.id === 'escalations' && <span className="count-badge">3</span>}
            </button>
          )
        })}
      </nav>
      <div className="sidebar-bottom">
        <button
          className={active === 'settings' ? 'nav-item active' : 'nav-item'}
          onClick={() => onSelect('settings')}
        >
          <Settings2 size={17} />
          <span>Settings</span>
        </button>
        <div className="profile">
          <Avatar initials="SG" tone="coral" small />
          <div><b>Sarah Goodman</b><small>Admin</small></div>
          <MoreHorizontal size={16} />
        </div>
      </div>
    </aside>
  )
}

export function Header({ title, eyebrow, onMenu }: { title: string; eyebrow: string; onMenu: () => void }) {
  return (
    <header className="topbar">
      <button className="mobile-menu" onClick={onMenu}><Menu size={20} /></button>
      <div><p className="eyebrow">{eyebrow}</p><h1>{title}</h1></div>
      <div className="top-actions">
        <button className="icon-button"><Search size={18} /></button>
        <button className="icon-button notification"><Bell size={18} /><i /></button>
        <button className="user-button">
          <Avatar initials="SG" tone="coral" small />
          <span>Sarah</span>
          <ChevronDown size={14} />
        </button>
      </div>
    </header>
  )
}

export function Metric({ label, value, change, icon: Icon, tone }: { label: string; value: string; change: string; icon: any; tone: string }) {
  return (
    <Glass className="metric">
      <div className={`metric-icon ${tone}`}><Icon size={18} /></div>
      <div><span>{label}</span><strong>{value}</strong><small className="positive">{change}</small></div>
      <ArrowUpRight size={16} className="metric-arrow" />
    </Glass>
  )
}

export function Dashboard({ onSelect }: { onSelect: (id: string) => void }) {
  return (
    <>
      <div className="alert-banner">
        <div className="alert-icon"><CircleAlert size={18} /></div>
        <div>
          <b>3 escalations need your attention</b>
          <span>Sarah and the agents are waiting on your decision.</span>
        </div>
        <button onClick={() => onSelect('escalations')}>Review inbox <ArrowUpRight size={15} /></button>
        <X size={16} className="alert-close" />
      </div>
      <div className="metrics-grid">
        <Metric label="Total Leads" value="1,284" change="+12.5% this month" icon={Users} tone="gold" />
        <Metric label="Active Conversations" value="86" change="+8.2% this week" icon={MessageSquare} tone="blue" />
        <Metric label="Deals Closed This Week" value="12" change="+3 from last week" icon={Check} tone="green" />
        <Metric label="Escalations Pending" value="3" change="Needs your attention" icon={CircleAlert} tone="coral" />
      </div>
      <div className="dashboard-grid">
        <Glass className="funnel-card">
          <div className="section-heading">
            <div><p className="eyebrow">PIPELINE OVERVIEW</p><h2>Where your leads are moving</h2></div>
            <button className="quiet-button">This week <ChevronDown size={14} /></button>
          </div>
          <div className="funnel">
            <div><span>Found</span><b>642</b><div className="funnel-bar bar-one" /></div>
            <div><span>Contacted</span><b>318</b><div className="funnel-bar bar-two" /></div>
            <div><span>Following Up</span><b>184</b><div className="funnel-bar bar-three" /></div>
            <div><span>Closing</span><b>86</b><div className="funnel-bar bar-four" /></div>
            <div><span>Won</span><b>12</b><div className="funnel-bar bar-five" /></div>
          </div>
        </Glass>
        <Glass className="activity-card">
          <div className="section-heading">
            <div><p className="eyebrow">LIVE ACTIVITY</p><h2>Agents at work</h2></div>
            <span className="live-status"><i /> Live</span>
          </div>
          <div className="activity-list">
            {[
              ['MC','Contact Finder','Found a high-fit contact at Northstar Labs','2m ago','gold'],
              ['ER','Outreach Agent','Call completed with Elena Rossi','8m ago','coral'],
              ['TA','Follow-Up Agent','Scheduled follow-up for Theo Adams','14m ago','green'],
              ['SG','Closing Agent','Proposal sent to Maya Chen','21m ago','blue']
            ].map(([initials, agent, text, time, tone]) => (
              <div className="activity-row" key={text}>
                <Avatar initials={initials} tone={tone} small />
                <div><b>{agent}</b><p>{text}</p></div>
                <time>{time}</time>
              </div>
            ))}
          </div>
          <button className="text-button">View all activity <ArrowUpRight size={14} /></button>
        </Glass>
      </div>
      <div className="bottom-grid">
        <Glass className="agent-health">
          <div className="section-heading">
            <div><p className="eyebrow">AGENT HEALTH</p><h2>Everything is flowing</h2></div>
            <Pill tone="green">All systems operational</Pill>
          </div>
          <div className="health-row"><span><i className="health-dot green-dot" />Contact Finding</span><span>Searching 24/7</span><b>98%</b></div>
          <div className="health-row"><span><i className="health-dot blue-dot" />Outreach Agent</span><span>86 calls active</span><b>94%</b></div>
          <div className="health-row"><span><i className="health-dot gold-dot" />Closing Agent</span><span>4 negotiations</span><b>91%</b></div>
        </Glass>
      </div>
    </>
  )
}

export function ContactFinding() {
  return (
    <>
      <div className="agent-hero">
        <div>
          <div className="agent-title">
            <span className="agent-orb"><Target size={20} /></span>
            <div><p className="eyebrow">CONTACT FINDING AGENT</p><h2>Find the right people, quietly.</h2></div>
          </div>
          <p className="muted">Your agent is scanning 2,480 companies for decision-makers who match your best customers.</p>
        </div>
        <div className="agent-status"><i /> Actively searching <span>·</span> Last scan 2m ago</div>
      </div>
      <div className="toolbar">
        <div className="search-field"><Search size={16} /><input placeholder="Search contacts or companies" /></div>
        <button className="filter-button"><Filter size={15} /> Filters <span>4</span></button>
        <button className="primary-button"><Plus size={16} /> Add to Outreach Queue</button>
      </div>
      <div className="filter-chips">
        <Pill tone="gold">SaaS <X size={12} /></Pill>
        <Pill tone="blue">VP+ <X size={12} /></Pill>
        <Pill tone="coral">United States <X size={12} /></Pill>
        <button className="text-button">Clear all</button>
      </div>
      <div className="contact-grid">
        {contacts.map(contact => (
          <Glass className="contact-card" key={contact.name}>
            <div className="contact-top">
              <Avatar initials={contact.initials} tone={contact.tone} />
              <button className="dots"><MoreHorizontal size={17} /></button>
            </div>
            <h3>{contact.name}</h3>
            <p>{contact.role}</p>
            <b className="company"><Building2 size={14} /> {contact.company}</b>
            <span className="location">{contact.location}</span>
            <div className="contact-bottom">
              <span>RELEVANCE</span>
              <strong>{contact.score}<small>/100</small></strong>
            </div>
            <div className="relevance"><i style={{ width: `${contact.score}%` }} /></div>
          </Glass>
        ))}
      </div>
    </>
  )
}

export function Outreach({ onSelect }: { onSelect?: (id: string) => void }) {
  const [expanded, setExpanded] = useState(1)
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">OUTREACH AGENT</p>
          <h2>Calls that feel like you.</h2>
          <p className="muted">Your queue is clear and moving. The agent has 18 calls lined up today.</p>
        </div>
        <button className="primary-button"><Plus size={16} /> Add call</button>
      </div>
      <div className="stat-strip">
        <div><span>CALLS TODAY</span><b>18</b><small className="positive">+4 vs yesterday</small></div>
        <div><span>INTEREST RATE</span><b>42%</b><small className="positive">+8.5% this week</small></div>
        <div><span>AVG. CALL DURATION</span><b>8m 42s</b><small>within target</small></div>
        <div className="strip-status"><i /> Agent is calling</div>
      </div>
      <Glass className="call-queue">
        <div className="section-heading">
          <div><p className="eyebrow">TODAY, SEPTEMBER 5</p><h2>Call queue</h2></div>
          <button className="quiet-button">All calls <ChevronDown size={14} /></button>
        </div>
        {[
          ['10:00 AM','Maya Chen','Northstar Labs','Completed','8m 24s','MC','gold'],
          ['10:30 AM','Elena Rossi','Verity Health','Completed','11m 02s','ER','coral'],
          ['11:00 AM','Marcus Bell','Harbor Systems','Pending','—','MB','blue'],
          ['11:30 AM','Theo Adams','Latticeworks','No answer','—','TA','green']
        ].map((call, i) => (
          <div key={call[1]}>
            <button
              className={`call-row ${expanded === i ? 'expanded' : ''}`}
              onClick={() => setExpanded(expanded === i ? -1 : i)}
            >
              <time>{call[0]}</time>
              <Avatar initials={call[5]} tone={call[6]} small />
              <div className="call-person"><b>{call[1]}</b><span>{call[2]}</span></div>
              <Pill tone={call[3] === 'Completed' ? 'green' : call[3] === 'Pending' ? 'blue' : 'muted'}>{call[3]}</Pill>
              <span className="duration">{call[4]}</span>
              <ChevronRight size={17} />
            </button>
            {expanded === i && call[3] === 'Completed' && (
              <div className="transcript">
                <div className="transcript-copy">
                  <p className="eyebrow">AI TRANSCRIPT</p>
                  <p><b>Maya:</b> We have been looking for a way to improve how our team handles inbound demand.</p>
                  <p><b>Sarah:</b> That is exactly where we help. Our agents qualify and route those conversations automatically.</p>
                  <p className="highlight"><Sparkles size={14} /> Strong buying signal: asked about implementation timeline.</p>
                </div>
                <div className="notes">
                  <p className="eyebrow">NOTES SUMMARY</p>
                  <div><span>Interest level</span><Pill tone="gold">Warm</Pill></div>
                  <div><span>Next step</span><b>Send proposal</b></div>
                  <div><span>Follow-up</span><b>Sep 9, 2026</b></div>
                  <button className="text-button" onClick={() => onSelect?.('lead')}>Open lead record <ArrowUpRight size={14} /></button>
                </div>
              </div>
            )}
          </div>
        ))}
      </Glass>
    </>
  )
}

export function FollowUp() {
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">FOLLOW-UP AGENT</p>
          <h2>Never let a warm lead cool.</h2>
          <p className="muted">18 thoughtful follow-ups scheduled across your pipeline.</p>
        </div>
        <button className="filter-button"><Filter size={15} /> Needs Escalation <span>3</span></button>
      </div>
      <div className="calendar-head">
        <button className="quiet-button">‹</button>
        <b>September 2026</b>
        <button className="quiet-button">›</button>
        <div className="calendar-legend">
          <span><i className="gold-dot" /> Warm</span>
          <span><i className="blue-dot" /> Cold</span>
          <span><i className="coral-dot" /> Escalated</span>
        </div>
      </div>
      <Glass className="timeline">
        <div className="timeline-day">
          <time>Today <small>SEP 5</small></time>
          <div className="timeline-items">
            <div className="follow-row warm">
              <Avatar initials="MC" tone="gold" small />
              <div><b>Maya Chen <Pill tone="gold">Warm</Pill></b><p>Send proposal recap and implementation timeline</p></div>
              <span>2:00 PM</span>
              <MoreHorizontal size={16} />
            </div>
            <div className="follow-row escalated">
              <Avatar initials="ER" tone="coral" small />
              <div><b>Elena Rossi <Pill tone="coral">Escalated</Pill></b><p>Review pricing objection before next touch</p></div>
              <span>4:30 PM</span>
              <MoreHorizontal size={16} />
            </div>
          </div>
        </div>
        <div className="timeline-day">
          <time>Tomorrow <small>SEP 6</small></time>
          <div className="timeline-items">
            <div className="follow-row cold">
              <Avatar initials="JB" tone="blue" small />
              <div><b>Jon Bellamy <Pill tone="blue">Cold</Pill></b><p>Share customer story from Clearpath AI</p></div>
              <span>10:15 AM</span>
              <MoreHorizontal size={16} />
            </div>
          </div>
        </div>
      </Glass>
    </>
  )
}

export function Closing() {
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">CLOSING AGENT</p>
          <h2>Deals are conversations, too.</h2>
          <p className="muted">4 active negotiations with a combined value of $182,400.</p>
        </div>
        <div className="closing-total"><span>PIPELINE VALUE</span><b>$182,400</b></div>
      </div>
      <div className="closing-grid">
        {[
          ['Northstar Labs','Maya Chen','$48,000','Contract Review','gold',['Security review','Final pricing','Legal approval'],'MC'],
          ['Harbor Systems','Marcus Bell','$32,500','In Negotiation','blue',['Confirm seats','ROI business case','Procurement'],'MB'],
          ['Latticeworks','Theo Adams','$64,000','Proposal Sent','green',['Proposal viewed','Schedule review call','Mutual action plan'],'TA']
        ].map(deal => (
          <Glass className="deal-card" key={deal[0]}>
            <div className="deal-top">
              <Pill tone={deal[3] === 'Contract Review' ? 'gold' : deal[3] === 'In Negotiation' ? 'blue' : 'green'}>{deal[3]}</Pill>
              <MoreHorizontal size={17} />
            </div>
            <h3>{deal[0]}</h3>
            <p className="deal-contact"><Avatar initials={deal[6] as string} tone={deal[3] === 'Contract Review' ? 'gold' : 'blue'} small /> {deal[1]}</p>
            <strong className="deal-value">{deal[2]}</strong>
            <div className="checklist">
              {(deal[5] as string[]).map((item, i) => (
                <div key={item}>
                  <span className={i === 0 ? 'checked' : ''}>{i === 0 && <Check size={12} />}</span>
                  {item}
                </div>
              ))}
            </div>
            <button className="review-button"><ShieldCheck size={15} /> Flag for Human Review</button>
          </Glass>
        ))}
      </div>
    </>
  )
}

export function LeadRecord() {
  return (
    <>
      <div className="lead-header">
        <div className="lead-person">
          <Avatar initials="MC" tone="gold" />
          <div><p className="eyebrow">LEAD RECORD</p><h2>Maya Chen</h2><p>VP of Revenue at Northstar Labs · Austin, TX</p></div>
        </div>
        <Pill tone="gold">Closing</Pill>
      </div>
      <Glass className="stepper-card">
        <div className="stepper">
          {[
            ['Found','Contact Finding','Sep 2','Contact identified from target account list.','done'],
            ['Contacted','Outreach Agent','Sep 3','Call completed. Maya shared that pipeline visibility is a priority.','done'],
            ['Following Up','Follow-Up Agent','Today','Proposal recap scheduled for 2:00 PM.','done'],
            ['Closing','Closing Agent','In progress','Contract review is underway. Waiting on security approval.','current'],
            ['Won / Lost','Orchestrator','Upcoming','The final step will be recorded here.','']
          ].map(item => (
            <div className={`step ${item[4]}`} key={item[0]}>
              <div className="step-marker">{item[4] === 'done' ? <Check size={13} /> : item[4] === 'current' ? <Sparkles size={13} /> : <span />}</div>
              <div className="step-content">
                <div><h3>{item[0]}</h3><Pill tone={item[4] === 'current' ? 'gold' : item[4] === 'done' ? 'green' : 'muted'}>{item[2]}</Pill></div>
                <b>{item[1]}</b>
                <p>{item[3]}</p>
                {item[4] === 'current' && <button className="text-button">View agent notes <ArrowUpRight size={14} /></button>}
              </div>
            </div>
          ))}
        </div>
      </Glass>
    </>
  )
}

export function Pipeline() {
  const stages = ['Found','Contacted','Following Up','Closing','Won','Lost']
  return (
    <>
      <div className="page-intro">
        <div><p className="eyebrow">LEAD PIPELINE</p><h2>Every opportunity, visible.</h2></div>
        <div className="toolbar-inline">
          <button className="quiet-button"><Filter size={14} /> All agents</button>
          <button className="quiet-button">Last 30 days <ChevronDown size={14} /></button>
        </div>
      </div>
      <div className="kanban">
        {stages.map(stage => (
          <div className="kanban-col" key={stage}>
            <div className="kanban-head">
              <span>{stage}</span>
              <b>{leads.filter(l => l.stage === stage).length}</b>
              <MoreHorizontal size={16} />
            </div>
            {leads.filter(l => l.stage === stage).map(lead => (
              <Glass className="kanban-card" key={lead.name}>
                <div className="kanban-card-top">
                  <Avatar initials={lead.initials} tone={lead.tone} small />
                  <Pill tone={stage === 'Won' ? 'green' : stage === 'Closing' ? 'gold' : stage === 'Lost' ? 'muted' : 'blue'}>{stage}</Pill>
                </div>
                <h3>{lead.name}</h3>
                <p>{lead.company}</p>
                <strong>{lead.value}</strong>
                <div className="kanban-foot">
                  <span>Last touched today</span>
                  <ChevronRight size={15} />
                </div>
              </Glass>
            ))}
          </div>
        ))}
      </div>
    </>
  )
}

export function Escalations() {
  const [resolved, setResolved] = useState<string[]>([])
  const items = [
    ['Pricing objection from Maya Chen','Closing Agent','Maya Chen · Northstar Labs','Maya asked for a 28% discount and wants to compare against an incumbent vendor. The agent recommends holding price and offering an annual commitment incentive.','12 min ago','MC','gold'],
    ['Unclear buying committee','Outreach Agent','Elena Rossi · Verity Health','Elena is excited, but mentioned that her co-founder signs off on all new tooling. Should we ask for an introduction?','38 min ago','ER','coral'],
    ['Contract clause needs review','Closing Agent','Marcus Bell · Harbor Systems','Marcus requested a custom data retention clause that falls outside the agent’s approval guardrails.','1 hr ago','MB','blue']
  ]
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">ESCALATION INBOX</p>
          <h2>Human judgment, right on time.</h2>
          <p className="muted">Your agents know when to ask. Here are the decisions waiting for you.</p>
        </div>
        <Pill tone="coral">3 need review</Pill>
      </div>
      <div className="escalation-list">
        {items.map(item => !resolved.includes(item[0]) && (
          <Glass className="escalation-card" key={item[0]}>
            <div className="escalation-left">
              <div className="new-mark">NEW</div>
              <Avatar initials={item[5]} tone={item[6]} />
              <div>
                <p className="eyebrow">{item[1]}</p>
                <h3>{item[0]}</h3>
                <b>{item[2]}</b>
                <p className="summary">{item[3]}</p>
                <time><Clock3 size={13} /> {item[4]}</time>
              </div>
            </div>
            <div className="escalation-actions">
              <button className="approve" onClick={() => setResolved([...resolved, item[0]])}><Check size={15} /> Approve</button>
              <button onClick={() => setResolved([...resolved, item[0]])}><X size={15} /> Reject</button>
              <button><UserRound size={15} /> Take over</button>
              <button><MessageSquare size={15} /> Message agent</button>
            </div>
          </Glass>
        ))}
      </div>
    </>
  )
}

export function ContactDatabase() {
  const [query, setQuery] = useState('')
  const filtered = contacts.filter(c => `${c.name} ${c.company} ${c.role}`.toLowerCase().includes(query.toLowerCase()))
  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">CONTACT DATABASE</p>
          <h2>Your relationship memory.</h2>
          <p className="muted">1,284 contacts across every agent and source.</p>
        </div>
        <button className="primary-button"><ArrowUpRight size={16} /> Export CSV</button>
      </div>
      <Glass className="database-card">
        <div className="database-toolbar">
          <div className="search-field">
            <Search size={16} />
            <input value={query} onChange={e => setQuery(e.target.value)} placeholder="Search by name, company, or role" />
          </div>
          <button className="quiet-button"><Filter size={14} /> Columns</button>
          <button className="quiet-button"><Filter size={14} /> Filter</button>
        </div>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th><input type="checkbox" /></th>
                <th>Name</th>
                <th>Designation</th>
                <th>Company</th>
                <th>Location</th>
                <th>Source</th>
                <th>Status</th>
                <th>Last Contacted</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map(c => (
                <tr key={c.name}>
                  <td><input type="checkbox" /></td>
                  <td><div className="table-name"><Avatar initials={c.initials} tone={c.tone} small /><b>{c.name}</b></div></td>
                  <td>{c.role}</td>
                  <td>{c.company}</td>
                  <td>{c.location}</td>
                  <td><span className="source"><Sparkles size={13} /> Agent</span></td>
                  <td><Pill tone={c.score > 90 ? 'gold' : 'blue'}>{c.score > 90 ? 'Warm' : 'New'}</Pill></td>
                  <td>Sep {c.score > 90 ? '4' : '2'}, 2026</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Glass>
    </>
  )
}

export function Settings() {
  const [subTab, setSubTab] = useState<'general' | 'contacts' | 'outreach' | 'followup' | 'closing' | 'orchestrator'>('general')
  const [toast, setToast] = useState('')

  // General Settings State
  const [workspaceName, setWorkspaceName] = useState('Goodman & Co.')
  const [workspaceDomain, setWorkspaceDomain] = useState('goodman.co')
  const [timezone, setTimezone] = useState('America/Chicago')
  const [team, setTeam] = useState([
    { name: 'Sarah Goodman', role: 'Owner / Admin', email: 'sarah@goodman.co', initials: 'SG', tone: 'coral' },
    { name: 'Maya Chen', role: 'VP of Revenue', email: 'maya@goodman.co', initials: 'MC', tone: 'gold' },
    { name: 'Marcus Bell', role: 'Revenue Operations', email: 'marcus@goodman.co', initials: 'MB', tone: 'blue' },
  ])
  const [newEmail, setNewEmail] = useState('')
  const [newRole, setNewRole] = useState('Sales Representative')
  const [showInvite, setShowInvite] = useState(false)
  const [notifEscalations, setNotifEscalations] = useState(true)
  const [notifDailyBriefing, setNotifDailyBriefing] = useState(true)
  const [notifWeeklySummary, setNotifWeeklySummary] = useState(true)
  const [notifHighValue, setNotifHighValue] = useState(true)

  // Contact Finding Settings State
  const [cfFormality, setCfFormality] = useState(3)
  const [cfDirectness, setCfDirectness] = useState(4)
  const [cfDailyQuota, setCfDailyQuota] = useState(50)
  const [cfMinFitScore, setCfMinFitScore] = useState(85)
  const [cfAutoEnrich, setCfAutoEnrich] = useState(true)
  const [cfEscalateEnterprise, setCfEscalateEnterprise] = useState(true)

  // Outreach Agent Settings State
  const [outreachFormality, setOutreachFormality] = useState(2) // 1=Casual, 5=Formal
  const [outreachDirectness, setOutreachDirectness] = useState(4) // 1=Direct, 5=Relationship
  const [outreachVoice, setOutreachVoice] = useState('Sarah (Warm Consultative)')
  const [outreachDailyLimit, setOutreachDailyLimit] = useState(25)
  const [outreachEscalateCompetitor, setOutreachEscalateCompetitor] = useState(true)
  const [outreachEscalateIntegration, setOutreachEscalateIntegration] = useState(true)
  const [outreachSentimentGuardrail, setOutreachSentimentGuardrail] = useState(true)

  // Follow-Up Agent Settings State
  const [fuFormality, setFuFormality] = useState(3)
  const [fuDirectness, setFuDirectness] = useState(4)
  const [fuTouch1Days, setFuTouch1Days] = useState('1')
  const [fuTouch2Days, setFuTouch2Days] = useState('4')
  const [fuTouch3Days, setFuTouch3Days] = useState('8')
  const [fuTouch4Days, setFuTouch4Days] = useState('14')
  const [fuMaxTouches, setFuMaxTouches] = useState('4')
  const [fuAutoPause, setFuAutoPause] = useState(true)
  const [fuEscalateUnanswered, setFuEscalateUnanswered] = useState(3)

  // Closing Agent Settings State
  const [closingFormality, setClosingFormality] = useState(4)
  const [closingDirectness, setClosingDirectness] = useState(3)
  const [closingMaxDiscount, setClosingMaxDiscount] = useState(15) // %
  const [closingMaxTermExt, setClosingMaxTermExt] = useState('30') // days
  const [closingPaymentTerms, setClosingPaymentTerms] = useState('Allow Net 45 without approval')
  const [closingMutualNDA, setClosingMutualNDA] = useState(true)
  const [closingStrictRedlines, setClosingStrictRedlines] = useState(true)

  // Orchestrator Settings State
  const [orchConfidence, setOrchConfidence] = useState(90)
  const [orchCoordMode, setOrchCoordMode] = useState('Adaptive Parallel Hand-off')
  const [orchBriefingTime, setOrchBriefingTime] = useState('8:30 AM')
  const [orchSafetySwitch, setOrchSafetySwitch] = useState(false)

  const triggerToast = (msg: string) => {
    setToast(msg)
    setTimeout(() => setToast(''), 3500)
  }

  const handleSave = () => {
    triggerToast('Settings & agent guardrails saved successfully.')
  }

  const handleReset = (tabKey: string) => {
    if (tabKey === 'general') {
      setWorkspaceName('Goodman & Co.')
      setWorkspaceDomain('goodman.co')
      setTimezone('America/Chicago')
      setNotifEscalations(true)
      setNotifDailyBriefing(true)
      setNotifWeeklySummary(true)
      setNotifHighValue(true)
    } else if (tabKey === 'contacts') {
      setCfFormality(3)
      setCfDirectness(4)
      setCfDailyQuota(50)
      setCfMinFitScore(85)
      setCfAutoEnrich(true)
      setCfEscalateEnterprise(true)
    } else if (tabKey === 'outreach') {
      setOutreachFormality(2)
      setOutreachDirectness(4)
      setOutreachVoice('Sarah (Warm Consultative)')
      setOutreachDailyLimit(25)
      setOutreachEscalateCompetitor(true)
      setOutreachEscalateIntegration(true)
      setOutreachSentimentGuardrail(true)
    } else if (tabKey === 'followup') {
      setFuFormality(3)
      setFuDirectness(4)
      setFuTouch1Days('1')
      setFuTouch2Days('4')
      setFuTouch3Days('8')
      setFuTouch4Days('14')
      setFuMaxTouches('4')
      setFuAutoPause(true)
      setFuEscalateUnanswered(3)
    } else if (tabKey === 'closing') {
      setClosingFormality(4)
      setClosingDirectness(3)
      setClosingMaxDiscount(15)
      setClosingMaxTermExt('30')
      setClosingPaymentTerms('Allow Net 45 without approval')
      setClosingMutualNDA(true)
      setClosingStrictRedlines(true)
    } else if (tabKey === 'orchestrator') {
      setOrchConfidence(90)
      setOrchCoordMode('Adaptive Parallel Hand-off')
      setOrchBriefingTime('8:30 AM')
      setOrchSafetySwitch(false)
    }
    triggerToast('Restored default presets for this tab.')
  }

  const handleInvite = (e: React.FormEvent) => {
    e.preventDefault()
    if (!newEmail.trim()) return
    const prefix = newEmail.split('@')[0]
    const formattedName = prefix.charAt(0).toUpperCase() + prefix.slice(1)
    const initials = (prefix.slice(0, 2)).toUpperCase()
    setTeam([...team, {
      name: formattedName,
      role: newRole,
      email: newEmail.trim(),
      initials,
      tone: 'green',
    }])
    setNewEmail('')
    setShowInvite(false)
    triggerToast(`Invitation sent to ${newEmail}`)
  }

  const settingsTabs = [
    { id: 'general', label: 'General', icon: Settings2, badge: 'Workspace' },
    { id: 'contacts', label: 'Contact Finding', icon: Target, badge: 'Agent' },
    { id: 'outreach', label: 'Outreach Agent', icon: Phone, badge: 'Agent' },
    { id: 'followup', label: 'Follow-Up Agent', icon: CalendarDays, badge: 'Agent' },
    { id: 'closing', label: 'Closing Agent', icon: ShieldCheck, badge: 'Agent' },
    { id: 'orchestrator', label: 'Orchestrator', icon: LayoutDashboard, badge: 'Core' },
  ] as const

  return (
    <>
      <div className="page-intro">
        <div>
          <p className="eyebrow">WORKSPACE & AGENT GOVERNANCE</p>
          <h2>Settings & Boundaries</h2>
          <p className="muted">Configure workspace parameters and fine-tune what each autonomous agent can decide independently.</p>
        </div>
        {toast && (
          <span className="pill pill-green" style={{ padding: '8px 14px', fontSize: '11px', animation: 'fadeIn .2s ease' }}>
            <Check size={14} /> {toast}
          </span>
        )}
      </div>

      <div className="settings-layout">
        {/* Left Sub-Navigation */}
        <Glass className="settings-subnav">
          <p className="nav-label" style={{ padding: '4px 12px 8px' }}>SECTIONS</p>
          {settingsTabs.map(t => {
            const Icon = t.icon
            const isAgent = t.badge === 'Agent' || t.badge === 'Core'
            return (
              <button
                key={t.id}
                className={`settings-subnav-btn ${subTab === t.id ? 'active' : ''}`}
                onClick={() => setSubTab(t.id)}
              >
                <Icon size={16} />
                <span>{t.label}</span>
                {isAgent && <Pill tone="gold" style={{ padding: '1px 5px', fontSize: '9px', marginLeft: 'auto' }}>Agent</Pill>}
              </button>
            )
          })}
        </Glass>

        {/* Right Content Panel */}
        <div className="settings-panel">
          {/* GENERAL TAB */}
          {subTab === 'general' && (
            <>
              <Glass className="settings-header-box">
                <p className="eyebrow">WORKSPACE PROFILE</p>
                <h2>Goodman & Co. Workspace</h2>
                <p className="muted">Manage your core team, regional settings, and operational notification triggers.</p>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Organization & Locale</h3>
                    <p className="settings-section-desc">Primary workspace identity and operating timezone.</p>
                  </div>
                </div>
                <div className="settings-grid-2">
                  <div className="settings-control-group">
                    <label className="settings-label">
                      WORKSPACE NAME
                    </label>
                    <input
                      className="settings-input"
                      value={workspaceName}
                      onChange={e => setWorkspaceName(e.target.value)}
                    />
                  </div>
                  <div className="settings-control-group">
                    <label className="settings-label">
                      COMPANY DOMAIN
                    </label>
                    <input
                      className="settings-input"
                      value={workspaceDomain}
                      onChange={e => setWorkspaceDomain(e.target.value)}
                    />
                  </div>
                </div>

                <div className="settings-control-group">
                  <label className="settings-label">
                    <span>OPERATIONAL TIMEZONE</span>
                    <span className="hint">Used for scheduled outreach & daily briefing recaps</span>
                  </label>
                  <select
                    className="settings-select"
                    value={timezone}
                    onChange={e => setTimezone(e.target.value)}
                  >
                    <option value="America/Chicago">America/Chicago (CST) — US Central (Default)</option>
                    <option value="America/New_York">America/New_York (EST) — US Eastern</option>
                    <option value="America/Denver">America/Denver (MST) — US Mountain</option>
                    <option value="America/Los_Angeles">America/Los_Angeles (PST) — US Pacific</option>
                    <option value="Europe/London">Europe/London (GMT) — United Kingdom</option>
                    <option value="Europe/Paris">Europe/Paris (CET) — Central Europe</option>
                    <option value="Asia/Singapore">Asia/Singapore (SGT) — Asia Pacific</option>
                  </select>
                </div>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Team Members & Access</h3>
                    <p className="settings-section-desc">Authorized operators with access to agent queues and escalation inboxes.</p>
                  </div>
                  <button className="quiet-button" onClick={() => setShowInvite(!showInvite)}>
                    <UserPlus size={14} /> Invite Member
                  </button>
                </div>

                {showInvite && (
                  <form onSubmit={handleInvite} style={{ display: 'flex', gap: 10, padding: 12, background: '#1c1713', border: '1px solid #4a3d31', borderRadius: 9, marginBottom: 8 }}>
                    <input
                      className="settings-input"
                      style={{ flex: 1 }}
                      placeholder="colleague@goodman.co"
                      value={newEmail}
                      onChange={e => setNewEmail(e.target.value)}
                      autoFocus
                    />
                    <select
                      className="settings-select"
                      style={{ width: 170 }}
                      value={newRole}
                      onChange={e => setNewRole(e.target.value)}
                    >
                      <option value="Sales Representative">Sales Rep</option>
                      <option value="Account Executive">Account Exec</option>
                      <option value="Revenue Operations">RevOps</option>
                      <option value="Admin">Admin</option>
                    </select>
                    <button type="submit" className="primary-button" style={{ padding: '8px 14px' }}>
                      Add
                    </button>
                  </form>
                )}

                <div className="settings-grid-1">
                  {team.map(member => (
                    <div className="team-member-row" key={member.email}>
                      <div className="team-member-info">
                        <Avatar initials={member.initials} tone={member.tone as any} small />
                        <div>
                          <b>{member.name}</b>
                          <span>{member.email}</span>
                        </div>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <Pill tone={member.role.includes('Admin') ? 'coral' : member.role.includes('VP') ? 'gold' : 'blue'}>
                          {member.role}
                        </Pill>
                        {member.role.includes('Admin') ? (
                          <span style={{ fontSize: 11, color: '#8f8276' }}>Owner</span>
                        ) : (
                          <button
                            type="button"
                            className="text-button"
                            style={{ color: '#8f8276', fontSize: 11 }}
                            onClick={() => setTeam(team.filter(t => t.email !== member.email))}
                          >
                            Remove
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Notification Preferences</h3>
                    <p className="settings-section-desc">Choose when and how Sarah Goodman is alerted to agent decisions.</p>
                  </div>
                </div>
                <div className="settings-grid-1">
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Instant Escalation Alerts</b>
                      <span>Immediately notify Sarah via SMS & Slack whenever an agent requires human judgment.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={notifEscalations} onChange={e => setNotifEscalations(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Daily 8:30 AM Executive Briefing</b>
                      <span>Deliver an orchestrated summary of conversations, replies, and closed opportunities every morning.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={notifDailyBriefing} onChange={e => setNotifDailyBriefing(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Weekly Pipeline Momentum Summary</b>
                      <span>Digest of overall funnel velocity, closed ARR, and objection patterns every Friday afternoon.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={notifWeeklySummary} onChange={e => setNotifWeeklySummary(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>VIP Account Alerts ($30k+ Pipeline Value)</b>
                      <span>Special notification whenever a high-tier prospect accepts an introductory call or opens a proposal.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={notifHighValue} onChange={e => setNotifHighValue(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                </div>
              </Glass>

              <Glass className="settings-footer-actions">
                <button className="quiet-button" onClick={() => handleReset('general')}>
                  <RotateCcw size={14} /> Reset to Defaults
                </button>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  {toast && <span className="saved-toast"><Check size={14} /> {toast}</span>}
                  <button className="primary-button" onClick={handleSave}>
                    <Save size={14} /> Save Changes
                  </button>
                </div>
              </Glass>
            </>
          )}

          {/* CONTACT FINDING AGENT TAB */}
          {subTab === 'contacts' && (
            <>
              <Glass className="settings-header-box">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span className="agent-orb" style={{ width: 36, height: 36 }}><Target size={18} /></span>
                  <div>
                    <p className="eyebrow">AUTONOMOUS AGENT CONFIGURATION</p>
                    <h2>Contact Finding Agent</h2>
                  </div>
                </div>
                <div className="settings-caption-badge">
                  <Info size={15} />
                  <span>Define what this agent can decide on its own — and what always comes back to you.</span>
                </div>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Discovery Persona & Search Filters</h3>
                    <p className="settings-section-desc">Govern how selectively this agent scans corporate networks and evaluates decision-maker relevance.</p>
                  </div>
                </div>

                <div className="tone-slider-wrap">
                  <div className="settings-label">
                    <span>EVALUATION PRECISION</span>
                    <span className="hint">
                      {cfDirectness <= 2 ? 'Broad Discovery (High Volume)' : cfDirectness === 3 ? 'Balanced Match' : 'Precision Fit (Strict Relevancy)'}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="1"
                    max="5"
                    value={cfDirectness}
                    onChange={e => setCfDirectness(Number(e.target.value))}
                    className="tone-slider"
                  />
                  <div className="tone-slider-labels">
                    <span className={cfDirectness === 1 ? 'active-tone' : ''}>Broad Discovery</span>
                    <span className={cfDirectness === 3 ? 'active-tone' : ''}>Balanced</span>
                    <span className={cfDirectness === 5 ? 'active-tone' : ''}>Laser Precision</span>
                  </div>
                </div>

                <div className="settings-grid-2">
                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>DAILY DISCOVERY QUOTA</span>
                      <span className="hint">{cfDailyQuota} verified leads / day</span>
                    </label>
                    <input
                      type="range"
                      min="15"
                      max="150"
                      step="5"
                      value={cfDailyQuota}
                      onChange={e => setCfDailyQuota(Number(e.target.value))}
                      className="tone-slider"
                    />
                  </div>
                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>MINIMUM FIT SCORE TO AUTO-APPROVE</span>
                      <span className="hint">{cfMinFitScore} / 100</span>
                    </label>
                    <input
                      type="range"
                      min="65"
                      max="95"
                      step="1"
                      value={cfMinFitScore}
                      onChange={e => setCfMinFitScore(Number(e.target.value))}
                      className="tone-slider"
                    />
                  </div>
                </div>

                <div className="settings-grid-1">
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Automatic Enrichment & Verification</b>
                      <span>Verify direct dial, work email, and recent executive appointments before adding to Outreach queue.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={cfAutoEnrich} onChange={e => setCfAutoEnrich(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Escalate Enterprise Accounts (&gt;$100M ARR / 500+ Staff)</b>
                      <span>Flag large multi-stakeholder enterprise accounts for Sarah to review strategy before first contact.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={cfEscalateEnterprise} onChange={e => setCfEscalateEnterprise(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                </div>

                {/* Live Preview Card */}
                <div className="preview-card-wrap">
                  <div className="preview-card-header">
                    <span><Sparkles size={13} /> LIVE AGENT DECISION SIMULATION</span>
                    <Pill tone="gold">Autonomous Action</Pill>
                  </div>
                  <div className="preview-message-box">
                    <p>
                      <strong>Target Evaluated:</strong> Maya Chen · VP of Revenue at Northstar Labs (Austin, TX)<br />
                      <strong>Calculated Fit Score:</strong> 96 / 100 · <strong>Configured Threshold:</strong> {cfMinFitScore} / 100<br />
                      <strong>Autonomous Decision:</strong> {96 >= cfMinFitScore ? 'Fit score exceeds threshold. Agent automatically enriches direct phone and queues for Outreach Agent at 10:00 AM.' : 'Fit score below threshold. Added to low-priority watchlist for human review.'}
                    </p>
                  </div>
                  <div className="preview-message-meta">
                    <span>Pacing limit: {cfDailyQuota} leads/day</span> · <span>Enrichment: {cfAutoEnrich ? 'Active' : 'Disabled'}</span>
                  </div>
                </div>
              </Glass>

              <Glass className="settings-footer-actions">
                <button className="quiet-button" onClick={() => handleReset('contacts')}>
                  <RotateCcw size={14} /> Reset to Defaults
                </button>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  {toast && <span className="saved-toast"><Check size={14} /> {toast}</span>}
                  <button className="primary-button" onClick={handleSave}>
                    <Save size={14} /> Save Changes
                  </button>
                </div>
              </Glass>
            </>
          )}

          {/* OUTREACH AGENT TAB */}
          {subTab === 'outreach' && (
            <>
              <Glass className="settings-header-box">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span className="agent-orb" style={{ width: 36, height: 36 }}><Phone size={18} /></span>
                  <div>
                    <p className="eyebrow">AUTONOMOUS AGENT CONFIGURATION</p>
                    <h2>Outreach Agent</h2>
                  </div>
                </div>
                <div className="settings-caption-badge">
                  <Info size={15} />
                  <span>Define what this agent can decide on its own — and what always comes back to you.</span>
                </div>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Voice Persona & Conversational Tone</h3>
                    <p className="settings-section-desc">Adjust the acoustic presence and conversational philosophy of outbound qualification calls.</p>
                  </div>
                </div>

                <div className="settings-grid-2">
                  <div className="tone-slider-wrap">
                    <div className="settings-label">
                      <span>FORMALITY</span>
                      <span className="hint">{outreachFormality <= 2 ? 'Casual & Approachable' : outreachFormality === 3 ? 'Professional' : 'Executive & Formal'}</span>
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="5"
                      value={outreachFormality}
                      onChange={e => setOutreachFormality(Number(e.target.value))}
                      className="tone-slider"
                    />
                    <div className="tone-slider-labels">
                      <span className={outreachFormality === 1 ? 'active-tone' : ''}>Casual</span>
                      <span className={outreachFormality === 3 ? 'active-tone' : ''}>Balanced</span>
                      <span className={outreachFormality === 5 ? 'active-tone' : ''}>Formal</span>
                    </div>
                  </div>

                  <div className="tone-slider-wrap">
                    <div className="settings-label">
                      <span>PITCH STYLE</span>
                      <span className="hint">{outreachDirectness <= 2 ? 'Direct & Pitch-forward' : outreachDirectness === 3 ? 'Problem-first' : 'Relationship & Consultative'}</span>
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="5"
                      value={outreachDirectness}
                      onChange={e => setOutreachDirectness(Number(e.target.value))}
                      className="tone-slider"
                    />
                    <div className="tone-slider-labels">
                      <span className={outreachDirectness === 1 ? 'active-tone' : ''}>Direct</span>
                      <span className={outreachDirectness === 3 ? 'active-tone' : ''}>Consultative</span>
                      <span className={outreachDirectness === 5 ? 'active-tone' : ''}>Relationship</span>
                    </div>
                  </div>
                </div>

                <div className="settings-grid-2">
                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>SYNTHESIZED VOICE PROFILE</span>
                    </label>
                    <select
                      className="settings-select"
                      value={outreachVoice}
                      onChange={e => setOutreachVoice(e.target.value)}
                    >
                      <option value="Sarah (Warm Consultative)">Sarah — Warm, natural executive tone (Default)</option>
                      <option value="Alex (Direct & Punchy)">Alex — Crisp, concise, data-driven delivery</option>
                      <option value="Jordan (Technical Specialist)">Jordan — Methodical, engineering empathy</option>
                    </select>
                  </div>

                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>MAX CONVERSATIONS PER DAY</span>
                      <span className="hint">{outreachDailyLimit} calls / day</span>
                    </label>
                    <input
                      type="range"
                      min="10"
                      max="60"
                      step="5"
                      value={outreachDailyLimit}
                      onChange={e => setOutreachDailyLimit(Number(e.target.value))}
                      className="tone-slider"
                    />
                  </div>
                </div>

                <div className="settings-section-title" style={{ marginTop: 10 }}>
                  <div>
                    <h3>Escalation & Safety Thresholds</h3>
                    <p className="settings-section-desc">Establish redlines where the voice agent yields control to Sarah Goodman.</p>
                  </div>
                </div>

                <div className="settings-grid-1">
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Escalate on Direct Competitor Named</b>
                      <span>If the prospect names an active incumbent (e.g. Outreach, Apollo, Salesloft), flag for custom competitive positioning.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={outreachEscalateCompetitor} onChange={e => setOutreachEscalateCompetitor(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Escalate Custom Security / Architecture Queries</b>
                      <span>Immediately route calls when prospective buyers ask for proprietary security questionnaires or bespoke API connectors.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={outreachEscalateIntegration} onChange={e => setOutreachEscalateIntegration(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Sentiment Guardrail (&gt;50% Friction)</b>
                      <span>Gracefully offer Sarah’s direct calendar if the prospect expresses annoyance or pushback.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={outreachSentimentGuardrail} onChange={e => setOutreachSentimentGuardrail(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                </div>

                {/* Live Preview Card */}
                <div className="preview-card-wrap">
                  <div className="preview-card-header">
                    <span><Sparkles size={13} /> LIVE CALL OPENING SIMULATION</span>
                    <Pill tone="blue">Voice Profile: {outreachVoice.split(' ')[0]}</Pill>
                  </div>
                  <div className="preview-message-box">
                    <p>
                      <strong>Agent ({outreachVoice.split(' ')[0]}):</strong> &ldquo;
                      {outreachFormality <= 2 && outreachDirectness >= 3
                        ? "Hey Maya, Sarah from SaleGoodman here! I was reading about Northstar’s revenue push this quarter — sounds like you guys are moving fast. Quick question: are your account execs spending too much time hunting contacts instead of closing?"
                        : outreachFormality >= 4 && outreachDirectness <= 2
                        ? "Good afternoon Ms. Chen. I am calling from SaleGoodman on behalf of Sarah Goodman. We track pipeline throughput for venture-backed B2B firms. Specifically, we help eliminate inbound routing bottlenecks. Would 15 minutes this Thursday make sense to discuss your quarterly targets?"
                        : "Hi Maya, this is Sarah with SaleGoodman. I saw Northstar Labs is expanding your sales team. We help revenue leaders qualify high-fit prospects without bogging down account executives. Do you have a quick moment to chat about how you're handling inbound demand?"
                      }&rdquo;
                    </p>
                  </div>
                  <div className="preview-message-meta">
                    <span>Tone: {outreachFormality <= 2 ? 'Casual' : outreachFormality >= 4 ? 'Formal' : 'Balanced'}</span> · <span>Style: {outreachDirectness <= 2 ? 'Direct' : outreachDirectness >= 4 ? 'Relationship-first' : 'Consultative'}</span>
                  </div>
                </div>
              </Glass>

              <Glass className="settings-footer-actions">
                <button className="quiet-button" onClick={() => handleReset('outreach')}>
                  <RotateCcw size={14} /> Reset to Defaults
                </button>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  {toast && <span className="saved-toast"><Check size={14} /> {toast}</span>}
                  <button className="primary-button" onClick={handleSave}>
                    <Save size={14} /> Save Changes
                  </button>
                </div>
              </Glass>
            </>
          )}

          {/* FOLLOW-UP AGENT TAB */}
          {subTab === 'followup' && (
            <>
              <Glass className="settings-header-box">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span className="agent-orb" style={{ width: 36, height: 36 }}><CalendarDays size={18} /></span>
                  <div>
                    <p className="eyebrow">AUTONOMOUS AGENT CONFIGURATION</p>
                    <h2>Follow-Up Agent</h2>
                  </div>
                </div>
                <div className="settings-caption-badge">
                  <Info size={15} />
                  <span>Define what this agent can decide on its own — and what always comes back to you.</span>
                </div>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Follow-Up Cadence & Timing Schedule</h3>
                    <p className="settings-section-desc">Design the precise interval between multi-channel follow-up touches across email and phone.</p>
                  </div>
                </div>

                <div className="cadence-grid">
                  <div className="cadence-node">
                    <b>TOUCH 1</b>
                    <span>Initial recap & timeline</span>
                    <select value={fuTouch1Days} onChange={e => setFuTouch1Days(e.target.value)}>
                      <option value="1">Day 1 post-call</option>
                      <option value="2">Day 2 post-call</option>
                      <option value="3">Day 3 post-call</option>
                    </select>
                  </div>
                  <div className="cadence-node">
                    <b>TOUCH 2</b>
                    <span>Value-add case study</span>
                    <select value={fuTouch2Days} onChange={e => setFuTouch2Days(e.target.value)}>
                      <option value="3">Day 3</option>
                      <option value="4">Day 4</option>
                      <option value="5">Day 5</option>
                      <option value="6">Day 6</option>
                    </select>
                  </div>
                  <div className="cadence-node">
                    <b>TOUCH 3</b>
                    <span>Proposal check-in</span>
                    <select value={fuTouch3Days} onChange={e => setFuTouch3Days(e.target.value)}>
                      <option value="7">Day 7</option>
                      <option value="8">Day 8</option>
                      <option value="10">Day 10</option>
                    </select>
                  </div>
                  <div className="cadence-node">
                    <b>TOUCH 4</b>
                    <span>Break-up & archive</span>
                    <select value={fuTouch4Days} onChange={e => setFuTouch4Days(e.target.value)}>
                      <option value="12">Day 12</option>
                      <option value="14">Day 14</option>
                      <option value="18">Day 18</option>
                    </select>
                  </div>
                </div>

                <div className="settings-grid-2">
                  <div className="tone-slider-wrap">
                    <div className="settings-label">
                      <span>COMMUNICATION FORMALITY</span>
                      <span className="hint">{fuFormality <= 2 ? 'Warm & Direct' : fuFormality === 3 ? 'Consultative' : 'Polite & Structured'}</span>
                    </div>
                    <input
                      type="range"
                      min="1"
                      max="5"
                      value={fuFormality}
                      onChange={e => setFuFormality(Number(e.target.value))}
                      className="tone-slider"
                    />
                    <div className="tone-slider-labels">
                      <span className={fuFormality === 1 ? 'active-tone' : ''}>Casual</span>
                      <span className={fuFormality === 3 ? 'active-tone' : ''}>Balanced</span>
                      <span className={fuFormality === 5 ? 'active-tone' : ''}>Formal</span>
                    </div>
                  </div>

                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>ESCALATE AFTER UNANSWERED TOUCHES</span>
                      <span className="hint">Escalate after {fuEscalateUnanswered} touches</span>
                    </label>
                    <select
                      className="settings-select"
                      value={fuEscalateUnanswered}
                      onChange={e => setFuEscalateUnanswered(Number(e.target.value))}
                    >
                      <option value={2}>Escalate after 2 unanswered touches</option>
                      <option value={3}>Escalate after 3 unanswered touches (Recommended)</option>
                      <option value={4}>Escalate after 4 unanswered touches</option>
                      <option value={5}>Do not escalate — auto-archive</option>
                    </select>
                  </div>
                </div>

                <div className="settings-grid-1">
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Auto-Pause on Inbound Activity</b>
                      <span>Immediately halt scheduled follow-up steps if the prospect replies, books a meeting, or triggers an out-of-office autoreply.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={fuAutoPause} onChange={e => setFuAutoPause(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                </div>

                {/* Live Preview Card */}
                <div className="preview-card-wrap">
                  <div className="preview-card-header">
                    <span><Sparkles size={13} /> SCHEDULED TOUCH PREVIEW</span>
                    <Pill tone="green">Touch 2 (Day {fuTouch2Days})</Pill>
                  </div>
                  <div className="preview-message-box">
                    <p>
                      <strong>Subject:</strong> {fuFormality <= 2 ? 'Quick thought on Northstar’s pipeline + customer story' : 'Relevant benchmark for Northstar Labs: Clearpath AI implementation'}<br />
                      <strong>Body:</strong> {fuFormality <= 2
                        ? "Hi Maya — hope your week is off to a great start! Sending over a quick 2-page recap of how Clearpath accelerated their sales cycle by 34% within 60 days of rolling out SaleGoodman. Would love to sync for 10 minutes tomorrow afternoon if you have questions!"
                        : "Dear Maya, following our discussion on Wednesday, I wanted to share the enclosed Clearpath AI case study documenting a 34% reduction in qualification cycle times. Does 2:00 PM tomorrow work for a brief review of implementation timelines?"
                      }
                    </p>
                  </div>
                  <div className="preview-message-meta">
                    <span>Active Cadence: Day {fuTouch1Days} → Day {fuTouch2Days} → Day {fuTouch3Days} → Day {fuTouch4Days}</span> · <span>Escalation: After {fuEscalateUnanswered} unanswered</span>
                  </div>
                </div>
              </Glass>

              <Glass className="settings-footer-actions">
                <button className="quiet-button" onClick={() => handleReset('followup')}>
                  <RotateCcw size={14} /> Reset to Defaults
                </button>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  {toast && <span className="saved-toast"><Check size={14} /> {toast}</span>}
                  <button className="primary-button" onClick={handleSave}>
                    <Save size={14} /> Save Changes
                  </button>
                </div>
              </Glass>
            </>
          )}

          {/* CLOSING AGENT TAB */}
          {subTab === 'closing' && (
            <>
              <Glass className="settings-header-box">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span className="agent-orb" style={{ width: 36, height: 36 }}><ShieldCheck size={18} /></span>
                  <div>
                    <p className="eyebrow">AUTONOMOUS AGENT CONFIGURATION</p>
                    <h2>Closing Agent</h2>
                  </div>
                </div>
                <div className="settings-caption-badge">
                  <Info size={15} />
                  <span>Define what this agent can decide on its own — and what always comes back to you.</span>
                </div>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Autonomous Negotiation Limits & Discount Authority</h3>
                    <p className="settings-section-desc">Set hard commercial ceilings. The agent will never exceed these parameters without an Escalation Inbox signoff.</p>
                  </div>
                </div>

                <div className="settings-grid-2">
                  <div className="tone-slider-wrap">
                    <div className="settings-label">
                      <span>MAXIMUM DISCOUNT WITHOUT APPROVAL</span>
                      <span className="hint" style={{ color: 'var(--primary)', fontWeight: 700 }}>{closingMaxDiscount}% discount</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="25"
                      step="1"
                      value={closingMaxDiscount}
                      onChange={e => setClosingMaxDiscount(Number(e.target.value))}
                      className="tone-slider"
                    />
                    <div className="tone-slider-labels">
                      <span className={closingMaxDiscount === 0 ? 'active-tone' : ''}>0% (Firm Price)</span>
                      <span className={closingMaxDiscount === 12 ? 'active-tone' : ''}>12%</span>
                      <span className={closingMaxDiscount === 25 ? 'active-tone' : ''}>25% Max</span>
                    </div>
                  </div>

                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>MAX CONTRACT TERM EXTENSION</span>
                      <span className="hint">{closingMaxTermExt} days beyond standard</span>
                    </label>
                    <select
                      className="settings-select"
                      value={closingMaxTermExt}
                      onChange={e => setClosingMaxTermExt(e.target.value)}
                    >
                      <option value="15">Max 15 days extension</option>
                      <option value="30">Max 30 days extension (Standard)</option>
                      <option value="45">Max 45 days extension</option>
                      <option value="60">Max 60 days extension (Requires pre-approval)</option>
                    </select>
                  </div>
                </div>

                <div className="settings-control-group">
                  <label className="settings-label">
                    <span>PAYMENT TERMS FLEXIBILITY</span>
                    <span className="hint">Invoicing concessions agent is authorized to offer</span>
                  </label>
                  <select
                    className="settings-select"
                    value={closingPaymentTerms}
                    onChange={e => setClosingPaymentTerms(e.target.value)}
                  >
                    <option value="Net 30 Only (Strict)">Strict Net 30 only — any variation escalates</option>
                    <option value="Allow Net 45 without approval">Allow Net 45 without approval (Recommended)</option>
                    <option value="Allow Net 60 with annual prepayment">Allow Net 60 only with full annual upfront prepay</option>
                  </select>
                </div>

                <div className="settings-grid-1">
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Permit Mutual NDA Signature on Goodman Standard Terms</b>
                      <span>Agent may counter-sign standard mutual non-disclosure agreements with approved counterparties.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={closingMutualNDA} onChange={e => setClosingMutualNDA(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Escalate All Legal Redlines & Indemnity Revisions</b>
                      <span>Any modification to liability caps, governing law, or intellectual property rights requires Sarah's signature.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={closingStrictRedlines} onChange={e => setClosingStrictRedlines(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                </div>

                {/* Live Preview Card */}
                <div className="preview-card-wrap">
                  <div className="preview-card-header">
                    <span><Sparkles size={13} /> LIVE NEGOTIATION CONCESSION SIMULATION</span>
                    <Pill tone="coral">Deal: Northstar Labs ($48,000)</Pill>
                  </div>
                  <div className="preview-message-box">
                    <p>
                      <strong>Scenario:</strong> Maya Chen requested a 20% discount ($9,600 reduction) and Net 60 invoicing.<br />
                      <strong>Agent Action:</strong> Your configured limit is <strong>{closingMaxDiscount}%</strong>.<br />
                      <strong>Agent Counter-Offer:</strong> &ldquo;Maya, I can honor an annual commitment incentive of {Math.min(closingMaxDiscount, 12)}% ($5,760 savings) along with {closingPaymentTerms}. For the additional requested discount, I’ve flagged this directly to Sarah Goodman for executive review.&rdquo;<br />
                      <strong>Escalation Inbox Status:</strong> Task automatically created in Sarah’s inbox with recommendation to approve 12% and hold price.
                    </p>
                  </div>
                  <div className="preview-message-meta">
                    <span>Discount Limit: {closingMaxDiscount}%</span> · <span>Max Term: {closingMaxTermExt} Days</span> · <span>Redlines: {closingStrictRedlines ? 'Strict Escalation' : 'Automated'}</span>
                  </div>
                </div>
              </Glass>

              <Glass className="settings-footer-actions">
                <button className="quiet-button" onClick={() => handleReset('closing')}>
                  <RotateCcw size={14} /> Reset to Defaults
                </button>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  {toast && <span className="saved-toast"><Check size={14} /> {toast}</span>}
                  <button className="primary-button" onClick={handleSave}>
                    <Save size={14} /> Save Changes
                  </button>
                </div>
              </Glass>
            </>
          )}

          {/* ORCHESTRATOR TAB */}
          {subTab === 'orchestrator' && (
            <>
              <Glass className="settings-header-box">
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span className="agent-orb" style={{ width: 36, height: 36 }}><LayoutDashboard size={18} /></span>
                  <div>
                    <p className="eyebrow">CORE PLATFORM BRAIN</p>
                    <h2>Orchestrator Coordination</h2>
                  </div>
                </div>
                <div className="settings-caption-badge">
                  <Info size={15} />
                  <span>Define what this agent can decide on its own — and what always comes back to you.</span>
                </div>
              </Glass>

              <Glass className="settings-section-card">
                <div className="settings-section-title">
                  <div>
                    <h3>Autonomous Handoff & Pipeline Routing</h3>
                    <p className="settings-section-desc">Control how the central brain delegates leads across Contact Finding, Outreach, Follow-Up, and Closing agents.</p>
                  </div>
                </div>

                <div className="tone-slider-wrap">
                  <div className="settings-label">
                    <span>DELEGATION CONFIDENCE THRESHOLD</span>
                    <span className="hint" style={{ color: 'var(--primary)', fontWeight: 700 }}>{orchConfidence}% confidence required</span>
                  </div>
                  <input
                    type="range"
                    min="75"
                    max="98"
                    step="1"
                    value={orchConfidence}
                    onChange={e => setOrchConfidence(Number(e.target.value))}
                    className="tone-slider"
                  />
                  <div className="tone-slider-labels">
                    <span className={orchConfidence <= 80 ? 'active-tone' : ''}>75% (Aggressive Autonomy)</span>
                    <span className={orchConfidence === 90 ? 'active-tone' : ''}>90% (Standard Balance)</span>
                    <span className={orchConfidence >= 95 ? 'active-tone' : ''}>98% (Conservative Human-in-the-loop)</span>
                  </div>
                </div>

                <div className="settings-grid-2">
                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>COORDINATION ARCHITECTURE</span>
                    </label>
                    <select
                      className="settings-select"
                      value={orchCoordMode}
                      onChange={e => setOrchCoordMode(e.target.value)}
                    >
                      <option value="Adaptive Parallel Hand-off">Adaptive Parallel Hand-off (Fastest Conversion)</option>
                      <option value="Strict Sequenced Gate">Strict Sequenced Gate (Approval at each step)</option>
                    </select>
                  </div>

                  <div className="settings-control-group">
                    <label className="settings-label">
                      <span>MORNING EXECUTIVE BRIEFING TIME</span>
                    </label>
                    <select
                      className="settings-select"
                      value={orchBriefingTime}
                      onChange={e => setOrchBriefingTime(e.target.value)}
                    >
                      <option value="7:30 AM">7:30 AM Local Time</option>
                      <option value="8:30 AM">8:30 AM Local Time (Default)</option>
                      <option value="9:30 AM">9:30 AM Local Time</option>
                    </select>
                  </div>
                </div>

                <div className="settings-grid-1">
                  <div className="settings-toggle-row">
                    <div className="settings-toggle-info">
                      <b>Emergency Outbound Safety Killswitch</b>
                      <span>Instantly pause all outbound calling and automated message transmissions across all agents with zero latency.</span>
                    </div>
                    <label className="settings-switch">
                      <input type="checkbox" checked={orchSafetySwitch} onChange={e => setOrchSafetySwitch(e.target.checked)} />
                      <span className="settings-slider-round" />
                    </label>
                  </div>
                </div>

                {/* Live Preview Card */}
                <div className="preview-card-wrap">
                  <div className="preview-card-header">
                    <span><Sparkles size={13} /> ORCHESTRATOR ROUTING PREVIEW</span>
                    <Pill tone="gold">Status: Operational (98%)</Pill>
                  </div>
                  <div className="preview-message-box">
                    <p>
                      <strong>Incoming Signal:</strong> High-intent visitor identified at Harbor Systems (Marcus Bell, CEO).<br />
                      <strong>Confidence Score:</strong> 94% · <strong>Threshold:</strong> {orchConfidence}%<br />
                      <strong>Routing Path:</strong> {94 >= orchConfidence ? 'Confidence exceeds 90% threshold. Orchestrator autonomously triggers Contact Finding verification and schedules Outreach Agent within 4 minutes.' : 'Confidence below threshold. Queued in Escalation Inbox for Sarah’s review.'}
                    </p>
                  </div>
                  <div className="preview-message-meta">
                    <span>Coordination Mode: {orchCoordMode}</span> · <span>Safety Switch: {orchSafetySwitch ? 'TRIGGERED (PAUSED)' : 'NORMAL'}</span>
                  </div>
                </div>
              </Glass>

              <Glass className="settings-footer-actions">
                <button className="quiet-button" onClick={() => handleReset('orchestrator')}>
                  <RotateCcw size={14} /> Reset to Defaults
                </button>
                <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                  {toast && <span className="saved-toast"><Check size={14} /> {toast}</span>}
                  <button className="primary-button" onClick={handleSave}>
                    <Save size={14} /> Save Changes
                  </button>
                </div>
              </Glass>
            </>
          )}
        </div>
      </div>
    </>
  )
}

export function Login({ onContinue }: { onContinue: () => void }) {
  return (
    <main className="login-page">
      <div className="login-shape shape-one" />
      <div className="login-shape shape-two" />
      <div className="login-card">
        <div className="login-brand"><span className="brand-mark"><Sparkles size={15} /></span><span>sale<strong>goodman</strong></span></div>
        <p className="eyebrow">WELCOME BACK</p>
        <h1>Your autonomous<br /><em>sales team.</em></h1>
        <p className="login-copy">A little less chasing. A lot more closing.</p>
        <label>Email address<input type="email" placeholder="you@company.com" /></label>
        <label>Password <a href="#forgot">Forgot?</a><input type="password" placeholder="••••••••••••" /></label>
        <button className="primary-button login-continue" onClick={onContinue}>Continue <ArrowUpRight size={16} /></button>
        <div className="divider"><span>or continue with</span></div>
        <button className="google-button"><span>G</span> Continue with Google</button>
        <small className="terms">By continuing, you agree to our <a href="#terms">Terms</a> and <a href="#privacy">Privacy Policy</a>.</small>
      </div>
      <p className="login-footer">SaleGoodman <span>·</span> Built for the beautifully ambitious</p>
    </main>
  )
}

export default function SaleGoodmanApp({ initialView = 'dashboard' }: { initialView?: string }) {
  const router = useRouter()
  const pathname = usePathname()
  const [mobileNav, setMobileNav] = useState(false)

  // Derive active view from pathname or initialView
  const currentView = useMemo(() => {
    if (!pathname || pathname === '/') return initialView || 'dashboard'
    const clean = pathname.replace(/^\//, '').split('/')[0]
    return clean || initialView || 'dashboard'
  }, [pathname, initialView])

  const [active, setActive] = useState<string>(currentView)

  useEffect(() => {
    if (currentView) {
      setActive(currentView)
    }
  }, [currentView])

  // Support hash routing fallback on root path
  useEffect(() => {
    if (typeof window === 'undefined') return
    const handleHash = () => {
      const hash = window.location.hash.replace('#', '').trim().toLowerCase()
      if (hash && hash !== active) {
        if (hash === 'login') {
          router.push('/login')
        } else if (nav.some(n => n.id === hash) || hash === 'lead' || hash === 'settings') {
          router.push(`/${hash}`)
        }
      }
    }
    handleHash()
    window.addEventListener('hashchange', handleHash)
    return () => window.removeEventListener('hashchange', handleHash)
  }, [active, router])

  const navigate = useCallback((id: string) => {
    setActive(id)
    setMobileNav(false)
    const target = id === 'dashboard' ? '/' : `/${id}`
    router.push(target)
  }, [router])

  const openLogin = useCallback(() => {
    router.push('/login')
  }, [router])

  const closeLogin = useCallback(() => {
    router.push('/')
  }, [router])

  if (active === 'login') {
    return <Login onContinue={closeLogin} />
  }

  const page = useMemo(() => {
    if (active === 'contacts') return <ContactFinding />
    if (active === 'outreach') return <Outreach onSelect={navigate} />
    if (active === 'followup') return <FollowUp />
    if (active === 'closing') return <Closing />
    if (active === 'lead') return <LeadRecord />
    if (active === 'pipeline') return <Pipeline />
    if (active === 'escalations') return <Escalations />
    if (active === 'database') return <ContactDatabase />
    if (active === 'settings') return <Settings />
    return <Dashboard onSelect={navigate} />
  }, [active, navigate])

  const current = nav.find(n => n.id === active)
  const headerTitle = active === 'lead' ? 'Lead Record' : active === 'settings' ? 'Settings & Preferences' : (current?.label || 'Orchestrator')
  const headerEyebrow = active === 'dashboard' ? 'GOOD MORNING, SARAH' : active === 'settings' ? 'WORKSPACE CONFIGURATION' : 'SALEGOODMAN WORKSPACE'

  return (
    <div className="app-shell">
      <Sidebar active={active} onSelect={navigate} />
      <div className={`mobile-sidebar ${mobileNav ? 'open' : ''}`}>
        <Sidebar active={active} onSelect={navigate} />
      </div>
      <main className="main-content">
        <Header
          title={headerTitle}
          eyebrow={headerEyebrow}
          onMenu={() => setMobileNav(!mobileNav)}
        />
        <div className="page-content">{page}</div>
      </main>
      <button className="floating-help" onClick={openLogin}>
        <Bot size={17} /> Ask SaleGoodman
      </button>
    </div>
  )
}
