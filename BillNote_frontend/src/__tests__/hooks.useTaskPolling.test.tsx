import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render } from '@testing-library/react'
import React from 'react'

vi.mock('@/store/taskStore', () => {
  const state = {
    tasks: [
      {
        id: 't1',
        status: 'PENDING',
        markdown: '',
        transcript: { full_text: '', language: '', raw: null, segments: [] },
        createdAt: new Date().toISOString(),
        audioMeta: { cover_url: '', duration: 0, file_path: '', platform: '', raw_info: null, title: '', video_id: '' },
        formData: { video_url: '', link: false, screenshot: false, platform: 'bilibili', quality: 'medium', model_name: 'm', provider_id: 'p' },
      },
    ],
    updateTaskContent: vi.fn(),
    updateTaskStatus: vi.fn(),
    removeTask: vi.fn(),
  }
  return {
    useTaskStore: (selector?: any) => {
      if (!selector) return state
      return selector(state)
    },
  }
})

vi.mock('@/services/note.ts', () => ({
  get_task_status: vi.fn(async (_id: string) => {
    return {
      status: 'SUCCESS',
      result: {
        markdown: '# OK',
        transcript: { full_text: 'hi', language: 'zh', raw: null, segments: [] },
        audio_meta: { title: 't', video_id: 'BV', platform: 'bilibili', duration: 1, file_path: '', cover_url: '', raw_info: {} },
      },
    }
  }),
}))

import { useTaskPolling } from '@/hooks/useTaskPolling'

function Probe() {
  useTaskPolling(10) // 快速轮询
  return <div>probe</div>
}

describe('useTaskPolling', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })
  afterEach(() => {
    vi.useRealTimers()
    vi.clearAllMocks()
  })

  it('should poll and update SUCCESS with content', async () => {
    const { useTaskStore } = await import('@/store/taskStore')
    const state = useTaskStore((s: any) => s)
    render(<Probe />)

    // 推动定时器执行轮询
    vi.advanceTimersByTime(30)

    // 断言 updateTaskContent 被以 SUCCESS 调用
    expect(state.updateTaskContent).toHaveBeenCalled()
    const calls = (state.updateTaskContent as any).mock.calls
    const last = calls[calls.length - 1]
    expect(last[0]).toBe('t1')
    expect(last[1].status).toBe('SUCCESS')
    expect(last[1].markdown).toBe('# OK')
    expect(last[1].transcript.full_text).toBe('hi')
  })
})