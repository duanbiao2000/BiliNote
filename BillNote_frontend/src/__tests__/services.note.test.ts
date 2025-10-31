import { vi, describe, it, expect } from 'vitest'

vi.mock('@/utils/request', () => {
  return {
    default: {
      post: vi.fn(async (url: string, payload: any) => {
        expect(url).toBe('/generate_note')
        expect(payload.platform).toBe('bilibili')
        // 模拟后端统一响应器返回的 data
        return { task_id: 'task-123' }
      }),
      get: vi.fn(),
    },
  }
})

import { generateNote } from '@/services/note'

describe('services/note.generateNote', () => {
  it('should call backend and return task_id', async () => {
    const res = await generateNote({
      video_url: 'https://www.bilibili.com/video/BV...',
      platform: 'bilibili',
      quality: 'medium',
      model_name: 'm',
      provider_id: 'p',
      format: [],
      style: 'minimal',
      grid_size: [3, 3],
    } as any)
    expect(res).toEqual({ task_id: 'task-123' })
  })
})


