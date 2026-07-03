import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
// Tailwind directives가 포함된 전역 스타일 파일 import
// 구조상 src/assets/styles/global.css 혹은 src/index.css 위치에 맞춰 수정
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)