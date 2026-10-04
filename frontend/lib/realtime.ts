/**
 * Supabase Realtime Subscriptions
 *
 * Enables live stream updates directly into the UI:
 * - Activity log entries (agent actions in real-time)
 * - Escalation notifications
 */

import { supabase } from './supabase'
import type { RealtimeChannel } from '@supabase/supabase-js'

export interface ActivityItem {
  id?: string
  agent_name: string
  description: string
  lead_id?: string
  initials?: string
  tone?: string
  created_at?: string
}

/**
 * Subscribe to new activity log events in the current workspace.
 */
export function subscribeToActivity(
  workspaceId: string,
  onNewActivity: (item: ActivityItem) => void
): RealtimeChannel {
  return supabase
    .channel('public:activity_log')
    .on(
      'postgres_changes',
      {
        event: 'INSERT',
        schema: 'public',
        table: 'activity_log',
        filter: `workspace_id=eq.${workspaceId}`,
      },
      (payload) => {
        onNewActivity(payload.new as ActivityItem)
      }
    )
    .subscribe()
}

/**
 * Subscribe to escalation updates.
 */
export function subscribeToEscalations(
  workspaceId: string,
  onEscalationChange: (payload: any) => void
): RealtimeChannel {
  return supabase
    .channel('public:escalation')
    .on(
      'postgres_changes',
      {
        event: '*',
        schema: 'public',
        table: 'escalation',
        filter: `workspace_id=eq.${workspaceId}`,
      },
      (payload) => {
        onEscalationChange(payload)
      }
    )
    .subscribe()
}
