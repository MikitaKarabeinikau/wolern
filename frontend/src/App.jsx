import ClerkProviderWithRoutes from "./features/auth/ClerkProviderWithRoutes.jsx";
import { Routes, Route } from "react-router-dom";
import { Layout } from "./layout/Layout.jsx";
import { AuthenticationPage } from "./features/auth/AuthenticationPage.jsx";
import { VocabulariesPanel } from "./features/vocabularies/VocabulariesPanel.jsx";
import { StatisticPanel } from "./features/statistics/StatisticPanel.jsx";
import { QuizGenerator } from "./features/quiz/QuizGenerator.jsx";
import { HomePanel } from "./features/home/HomePanel.jsx";
import { ExercisesPanel } from "./features/exerciese/ExercisesPanel.jsx";
import { ScannerPanel } from "./features/scanner/ScannerPanel.jsx";
import "./App.css";

function App() {
  return (
    <ClerkProviderWithRoutes>
      <Routes>
        <Route path="/sign-in/*" element={<AuthenticationPage />} />
        <Route path="/sign-up" element={<AuthenticationPage />} />

        <Route element={<Layout />}>
          <Route path="/" element={<HomePanel />} />
          <Route path="/vocabularies" element={<VocabulariesPanel />} />
          <Route path="/statistics" element={<StatisticPanel />} />
          <Route path="/quiz" element={<QuizGenerator />} />
          <Route path="/exercises" element={<ExercisesPanel />} />
          <Route path="/scanner" element={<ScannerPanel />} />
        </Route>
      </Routes>
    </ClerkProviderWithRoutes>
  );
}

export default App;
