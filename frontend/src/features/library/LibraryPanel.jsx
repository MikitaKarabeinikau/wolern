import React, { useRef } from "react";

export function LibraryPanel() {
  const fileInputRef = useRef();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    // Do something with the file (e.g., upload to server or Google Drive)
    console.log("Selected file:", file);
  };

  return (
    <div>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileChange}
        style={{ display: "block", margin: "1em 0" }}
      />
      {/* Optionally, add a button to trigger file selection */}
      <button onClick={() => fileInputRef.current.click()}>Add File</button>
    </div>
  );
}
