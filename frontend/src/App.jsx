import ClerkProviderWithRoutes from './auth/ClerkProviderWithRoutes.jsx'
import { Routes, Route } from 'react-router-dom' 
import { Layout } from './layout/Layout.jsx'
import { AuthenticationPage } from './auth/AuthenticationPage.jsx'
import { VocabulariesPanel } from './vocabularies/VocabulariesPanel.jsx'
import { StatisticPanel } from './statistics/StatisticPanel.jsx'
import { QuizGenerator } from './quiz/QuizGenerator.jsx' 
import { HomePanel } from './home/HomePanel.jsx'
import { ExercisesPanel } from './exerciese/ExercisesPanel.jsx'
import './App.css'


function App() {
// Wrap your app with ClerkProviderWithRouters. All your routes should be inside this.
  return <ClerkProviderWithRoutes>
      <Routes>

        <Route path="/sign-in/*" element={<AuthenticationPage />} />
        <Route path="/sign-up" element={<AuthenticationPage />} />
        
        <Route element={<Layout />}>
          <Route path="/" element={<HomePanel />} />
          <Route path="/vocabularies" element={<VocabulariesPanel />} />
          <Route path="/statistics" element={<StatisticPanel />} />
          <Route path="/quiz" element={<QuizGenerator />} />
          <Route path="/exercises" element={<ExercisesPanel />} />
          {/* <Route path="/scanner" element={<ScannerPanel />} /> */}
        </Route>
      </Routes>
  </ClerkProviderWithRoutes>
}

export default App
