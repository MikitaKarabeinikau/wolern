import { useState } from 'react'
import './App.css'
import ClerkProviderWithRouters from './auth/ClerkProviderWithRouters.jsx'
import { Routes, Route } from 'react-router-dom' 
import { Layout } from './layout/Layout.jsx'
import { AuthenticationPage } from './auth/AuthenticationPage.jsx'
import { VocabulariesPanel } from './vocabularies/VocabulariesPanel.jsx'
import { StatisticPanel } from './statistics/StatisticPanel.jsx'


function App() {
  const [count, setCount] = useState(0)
// Wrap your app with ClerkProviderWithRouters. All your routes should be inside this.
  return <ClerkProviderWithRouters>
    <Routes>
      <Route path="/sign-in/*" element={<AuthenticationPage/>} />
      <Route path="/sign-up/*" element={<AuthenticationPage/>} />
      <Route element={<Layout/>}>
        <Route path="/" element={<VocabulariesPanel/>} />
        <Route path="/statistics" element={<StatisticPanel/>} />
      </Route>
    </Routes>
  </ClerkProviderWithRouters>
}

export default App
