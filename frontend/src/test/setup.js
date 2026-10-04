import '@testing-library/jest-dom'
import { vi } from 'vitest'

// Mock HTMLMediaElement methods
window.HTMLMediaElement.prototype.play = vi.fn().mockResolvedValue(undefined)
window.HTMLMediaElement.prototype.pause = vi.fn()

// Mock URL.createObjectURL and revokeObjectURL
window.URL.createObjectURL = vi.fn(() => 'blob:mock-url')
window.URL.revokeObjectURL = vi.fn()

// Mock navigator.mediaDevices
Object.defineProperty(navigator, 'mediaDevices', {
  value: {
    getUserMedia: vi.fn().mockResolvedValue({
      getTracks: () => [
        { stop: vi.fn(), enabled: true },
        { stop: vi.fn(), enabled: true }
      ]
    }),
    enumerateDevices: vi.fn().mockResolvedValue([]),
  },
  configurable: true,
})

// Mock MediaRecorder
class MockMediaRecorder {
  constructor(stream, options) {
    this.stream = stream
    this.options = options
    this.state = 'inactive'
    this.ondataavailable = null
    this.onstop = null
  }
  start() {
    this.state = 'recording'
  }
  stop() {
    this.state = 'inactive'
    if (this.onstop) this.onstop()
  }
  pause() {
    this.state = 'paused'
  }
  resume() {
    this.state = 'recording'
  }
}
MockMediaRecorder.isTypeSupported = vi.fn().mockReturnValue(true)
global.MediaRecorder = MockMediaRecorder
window.MediaRecorder = MockMediaRecorder

// Mock window.print
window.print = vi.fn()

// Mock speechSynthesis
window.speechSynthesis = {
  speak: vi.fn(),
  cancel: vi.fn(),
}
global.SpeechSynthesisUtterance = vi.fn()
window.SpeechSynthesisUtterance = vi.fn()

// Mock matchMedia
if (!window.matchMedia) {
  window.matchMedia = vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  }))
}
