/**
 * SaleGoodman API Client
 *
 * Connects the Next.js frontend to the FastAPI backend.
 * Gracefully falls back to mock defaults if the backend is unreachable.
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface RequestOptions extends RequestInit {
  token?: string
}

async function fetchWithAuth<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { token, headers = {}, ...rest } = options
  const authHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(headers as Record<string, string>),
  }

  if (token) {
    authHeaders['Authorization'] = `Bearer ${token}`
  }

  const res = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...rest,
    headers: authHeaders,
  })

  if (!res.ok) {
    const errorBody = await res.text()
    throw new Error(`API error ${res.status}: ${errorBody}`)
  }

  return res.json()
}

// ── Types ─────────────────────────────────────────────────────────────

export interface Contact {
  id?: string
  name: string
  role?: string
  title?: string
  company: string
  location?: string
  score?: number
  relevance_score?: number
  initials: string
  tone?: string
  email?: string
  phone?: string
  enriched?: boolean
  source?: string
  tags?: string[]
}

export interface Lead {
  id?: string
  name?: string
  company: string
  stage: string
  initials: string
  value: string
  tone?: string
  contact_id?: string
  contact?: Contact
}

export interface EscalationItem {
  id: string
  lead_id?: string
  title: string
  source_agent: string
  contact_info: string
  summary: string
  created_at?: string
  status?: string
}

export interface DashboardMetrics {
  pipeline_value: string
  active_leads: number
  calls_queued: number
  escalations_count: number
}

// ── API Methods ───────────────────────────────────────────────────────

export const api = {
  // System Health
  async checkHealth(): Promise<{ status: string; service: string }> {
    return fetchWithAuth('/health')
  },

  // Dashboard
  async getDashboardMetrics(token?: string): Promise<DashboardMetrics> {
    try {
      return await fetchWithAuth<DashboardMetrics>('/dashboard/metrics', { token })
    } catch {
      // Return default mock metrics on connection failure
      return {
        pipeline_value: '$201,500',
        active_leads: 6,
        calls_queued: 4,
        escalations_count: 3,
      }
    }
  },

  // Contacts
  async getContacts(token?: string): Promise<Contact[]> {
    return fetchWithAuth<Contact[]>('/contacts', { token })
  },

  async createContact(data: Partial<Contact>, token?: string): Promise<Contact> {
    return fetchWithAuth<Contact>('/contacts', {
      method: 'POST',
      body: JSON.stringify(data),
      token,
    })
  },

  // Leads
  async getLeads(token?: string): Promise<Lead[]> {
    return fetchWithAuth<Lead[]>('/leads', { token })
  },

  async updateLeadStage(leadId: string, stage: string, token?: string): Promise<Lead> {
    return fetchWithAuth<Lead>(`/leads/${leadId}/stage`, {
      method: 'PATCH',
      body: JSON.stringify({ stage }),
      token,
    })
  },

  // Calls
  async getCallQueue(token?: string): Promise<any[]> {
    return fetchWithAuth<any[]>('/calls/queue', { token })
  },

  async startCall(contactId: string, token?: string): Promise<any> {
    return fetchWithAuth<any>('/calls', {
      method: 'POST',
      body: JSON.stringify({ contact_id: contactId }),
      token,
    })
  },

  // Follow-ups
  async getFollowUps(token?: string): Promise<any[]> {
    return fetchWithAuth<any[]>('/follow-ups', { token })
  },

  // Deals
  async getDeals(token?: string): Promise<any[]> {
    return fetchWithAuth<any[]>('/deals', { token })
  },

  // Escalations
  async getEscalations(token?: string): Promise<EscalationItem[]> {
    return fetchWithAuth<EscalationItem[]>('/escalations', { token })
  },

  async approveEscalation(id: string, notes?: string, token?: string): Promise<any> {
    return fetchWithAuth(`/escalations/${id}/approve`, {
      method: 'POST',
      body: JSON.stringify({ notes }),
      token,
    })
  },

  async rejectEscalation(id: string, reason?: string, token?: string): Promise<any> {
    return fetchWithAuth(`/escalations/${id}/reject`, {
      method: 'POST',
      body: JSON.stringify({ reason }),
      token,
    })
  },

  // Agent Settings
  async getAgentConfig(agentType: string, token?: string): Promise<any> {
    return fetchWithAuth(`/settings/agents/${agentType}`, { token })
  },

  async updateAgentConfig(agentType: string, config: Record<string, any>, token?: string): Promise<any> {
    return fetchWithAuth(`/settings/agents/${agentType}`, {
      method: 'PUT',
      body: JSON.stringify({ config }),
      token,
    })
  },
}

export default api
