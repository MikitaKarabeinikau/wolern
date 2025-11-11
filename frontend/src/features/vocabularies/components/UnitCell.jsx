import React, { useState } from "react";
import "../../../../styles/UnitCell.css";

/**
 * A generic component to display, edit, and delete a single piece of content.
 * @param {object} item - The data object. Must have an 'id' and a 'text' property.
 * @param {function} onUpdate - Callback function to execute on update. Receives (id, newText).
 * @param {function} onDelete - Callback function to execute on delete. Receives (id).
 */

function UnitCell({ item, onUpdate, onDelete, isLoading = false }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editedText, setEditedText] = useState(item.text);

  const handleDelete = () => {
    console.log(`Delete requested for item ID: ${item.id}`);
    onDelete(item.id);
  };
  const handleUpdate = () => {
    onUpdate(item.id, editedText);
    setIsEditing(false);
  };

  const startEditing = () => {
    setEditedText(item.text);
    setIsEditing(true);
  };

  const cancelEditing = () => {
    setIsEditing(false);
  };

  if (isEditing) {
    return (
      <div className="unit-cell editing">
        <p className="unit-cell-text">{item.text}</p>
        <textarea
          value={editedText}
          onChange={(e) => setEditedText(e.target.value)}
          className="unit-cell-textarea"
          disabled={isLoading}
        />
        <div className="unit-cell-actions">
          <button
            onClick={handleUpdate}
            className="unit-cell-btn save"
            disabled={isLoading}
          >
            Save
          </button>
          <button
            onClick={cancelEditing}
            className="unit-cell-btn cancel"
            disabled={isLoading}
          >
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="unit-cell">
      <span className="unit-cell-text"> {item.text}</span>
      <div className="unit-cell-actions">
        <button
          onClick={startEditing}
          className="unit-cell-btn edit"
          disabled={isLoading}
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="unit-cell-btn delete"
          disabled={isLoading}
        >
          Delete
        </button>
      </div>
    </div>
  );
}

export default UnitCell;
