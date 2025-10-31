import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import React from 'react'
import { MemoryRouter } from 'react-router-dom'

// Mock Model Store（提供一个可选模型）
vi.mock('@/store/modelStore', () => {
  return {
    useModelStore: (selector?: any) => {
      const state = {
        modelList: [{ id: '1', model_name: 'gpt-mini', provider_id: 'provider-1' }],
        loadEnabledModels: vi.fn(),
        showFeatureHint: false,
        setShowFeatureHint: vi.fn(),
      }
      return selector ? selector(state) : state
    },
  }
})

// Mock Task Store（拦截 addPendingTask、retry）
const addPendingTask = vi.fn()
const retryTask = vi.fn()
vi.mock('@/store/taskStore', () => {
  const state = {
    addPendingTask,
    retryTask,
    currentTaskId: null,
    setCurrentTask: vi.fn(),
    getCurrentTask: vi.fn(() => null),
  }
  return {
    useTaskStore: (selector?: any) => (selector ? selector(state) : state),
  }
})

// Mock 网络服务 generateNote
const generateNote = vi.fn(async () => ({ task_id: 'task-abc' }))
vi.mock('@/services/note.ts', () => ({
  generateNote,
}))

// 由于表单用到了大量 ui 组件，这里将部分基础 UI 组件 mock 成最小实现
vi.mock('@/components/ui/input.tsx', () => ({
  Input: (props: any) => <input aria-label="input" {...props} />,
}))
vi.mock('@/components/ui/textarea.tsx', () => ({
  Textarea: (props: any) => <textarea aria-label="textarea" {...props} />,
}))
vi.mock('@/components/ui/button.tsx', () => ({
  Button: (props: any) => <button {...props} />,
}))
vi.mock('@/components/ui/checkbox.tsx', () => ({
  Checkbox: (props: any) => <input type="checkbox" aria-label="checkbox" checked={!!props.checked} onChange={e => props.onCheckedChange?.(e.target.checked)} />,
}))
vi.mock('@/components/ui/select.tsx', () => {
  const Select = (p: any) => <div>{p.children}</div>
  const SelectTrigger = (p: any) => <div {...p} />
  const SelectContent = (p: any) => <div {...p} />
  const SelectItem = (p: any) => <div role="option" onClick={() => p.onClick?.()} {...p} />
  const SelectValue = (p: any) => <span {...p} />
  return { Select, SelectTrigger, SelectContent, SelectItem, SelectValue }
})
vi.mock('@/components/ui/form.tsx', () => {
  const Form = (p: any) => <div>{p.children}</div>
  const FormField = (p: any) => <div>{p.render({ field: { value: p.value, onChange: p.onChange } })}</div>
  const FormItem = (p: any) => <div>{p.children}</div>
  const FormLabel = (p: any) => <label>{p.children}</label>
  const FormControl = (p: any) => <div>{p.children}</div>
  const FormMessage = (p: any) => <div>{p.children}</div>
  return { Form, FormField, FormItem, FormLabel, FormControl, FormMessage }
})
vi.mock('@/components/ui/tooltip.tsx', () => {
  const Tooltip = (p: any) => <div>{p.children}</div>
  const TooltipTrigger = (p: any) => <span>{p.children}</span>
  const TooltipContent = (p: any) => <div>{p.children}</div>
  const TooltipProvider = (p: any) => <div>{p.children}</div>
  return { Tooltip, TooltipTrigger, TooltipContent, TooltipProvider }
})
vi.mock('@/components/ui/scroll-area.tsx', () => ({
  ScrollArea: (p: any) => <div>{p.children}</div>,
}))

// mock 其它无关组件
vi.mock('@/pages/HomePage/components/StepBar.tsx', () => ({ default: () => <div /> }))
vi.mock('antd', () => ({ Alert: (p: any) => <div>{p.children}</div>, message: { success: vi.fn(), error: vi.fn() } }))

// 引入待测组件
import NoteForm from '@/pages/HomePage/components/NoteForm'

describe('NoteForm validation and submit', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })
  afterEach(() => {
    vi.clearAllMocks()
  })

  it('should validate video_url required and submit successfully', async () => {
    render(
      <MemoryRouter>
        <NoteForm />
      </MemoryRouter>
    )

    // 填写必要字段：video_url
    const inputs = screen.getAllByLabelText('input')
    const urlInput = inputs[0]
    fireEvent.change(urlInput, { target: { value: 'https://www.bilibili.com/video/BVxxxx' } })

    // 提交
    const submitBtn = screen.getByRole('button')
    fireEvent.click(submitBtn)

    await waitFor(() => {
      expect(generateNote).toHaveBeenCalled()
      expect(addPendingTask).toHaveBeenCalled()
      const args = (addPendingTask as any).mock.calls[0]
      expect(args[0]).toBe('task-abc') // task_id
      expect(args[1]).toBe('bilibili') // platform
    })
  })
})