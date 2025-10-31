import { describe, it, expect } from 'vitest'
import { useTaskStore } from '@/store/taskStore'

describe('taskStore markdown versioning', () => {
  it('wraps string markdown into version list and appends new versions', () => {
    const id = 't1'
    // 初始化一个任务
    useTaskStore.setState({
      tasks: [
        {
          id,
          status: 'PENDING',
          markdown: '',
          transcript: { full_text: '', language: '', raw: null, segments: [] },
          createdAt: new Date().toISOString(),
          audioMeta: { cover_url: '', duration: 0, file_path: '', platform: '', raw_info: null, title: '', video_id: '' },
          formData: { video_url: '', link: false, screenshot: false, platform: 'bilibili', quality: 'medium', model_name: 'm', provider_id: 'p' },
        },
      ],
      currentTaskId: id,
    } as any)

    // 第一次成功：字符串 markdown -> 版本化
    useTaskStore.getState().updateTaskContent(id, { status: 'SUCCESS', markdown: '# v1' } as any)
    let t = useTaskStore.getState().getCurrentTask()!
    expect(Array.isArray(t.markdown)).toBe(true)
    expect((t.markdown as any[]).length).toBe(1)
    expect((t.markdown as any[])[0].content).toBe('# v1')

    // 再次成功：应在前面追加新版本
    useTaskStore.getState().updateTaskContent(id, { status: 'SUCCESS', markdown: '# v2' } as any)
    t = useTaskStore.getState().getCurrentTask()!
    expect((t.markdown as any[]).length).toBe(2)
    expect((t.markdown as any[])[0].content).toBe('# v2')
    expect((t.markdown as any[])[1].content).toBe('# v1')
  })
})


