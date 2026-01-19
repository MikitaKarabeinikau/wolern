import React, { useState, useEffect, useTransition } from "react";
import "../../../styles/vocabulary/VocabularyPanel.css";
export function VocabularyPanel() {
  return (
    <div className="vocabulary-panel">
      <div className="vocabulary-add-panel">add panel</div>
      <div className="vocabulary-filters-panel">filters panel</div>
      <div className="vocabulary-words-header-panel">sort and search panel</div>
      <div className="vocabulary-words-body-panel">words panel</div>
      <div className="vocabulary-words-footer-panel">words pages</div>
    </div>
  );
}
