import React, { useState } from "react";
import '../../styles/Word.css';

const AddInfo = ({ withCategory, category_name, categories, onAddInfo, onAddCategory }) => {
  const [categorySet, setCategorySet] = useState(new Set(categories || []));
  const [info, setInfo] = useState("");
  const [isCategoryMenuOpen, setIsCategoryMenuOpen] = useState(false);
  const [categorySelected, setCategorySelected] = useState((categories && categories[0]) || "");

  const handleOpenCategoryMenu = () => {
    setIsCategoryMenuOpen(true);
  };

  const handleCloseCategoryMenu = () => {
    setIsCategoryMenuOpen(false);
  };

  const handleToggleCategoryMenu = () => {
    setIsCategoryMenuOpen(!isCategoryMenuOpen);
  };

  const handleChangCategory = (newCategory) => {
    setCategorySelected(newCategory);
    setIsCategoryMenuOpen(false);
  };

  const handleAddInfo = () => {
    if (withCategory) {
      if (!categorySelected.trim()) {
        alert(`Please select a ${category_name}`);
        return;
      }
    }
    if (!info.trim()) {
      alert(`Please enter a valid ${category_name}`);
      return;
    }
    onAddInfo(categorySelected, info);
    setInfo("");
  };

  const handleNewCategory = () => {
    const newCategory = prompt("Enter new category:");
    if (newCategory && newCategory.trim()) {
      const trimmedCategory = newCategory.trim();
      if (!categorySet.has(trimmedCategory)) {
        const updatedSet = new Set([...categorySet, trimmedCategory]);
        setCategorySet(updatedSet);
        setCategorySelected(trimmedCategory);
        if (onAddCategory) {
          onAddCategory(trimmedCategory);
        }
      } else {
        alert("This category already exists!");
      }
    }
    setIsCategoryMenuOpen(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleAddInfo();
    }
  };

  if (withCategory) {
    return (
      <div className="add-container">
        <div className="input-section">
          <div className="category-selector">
            <label>
              Category: <strong>{categorySelected || "None"}</strong>
            </label>
            <button
              className="change-category-btn"
              onClick={handleToggleCategoryMenu}
            >
              {isCategoryMenuOpen ? "Close Menu" : `Change ${category_name} `}
            </button>
          </div>

          <div className="input">
            <input
              type="text"
              placeholder={`Enter ${category_name}`}
              value={info}
              onChange={(e) => setInfo(e.target.value)}
              onKeyDown={handleKeyDown}
              className="field"
            />
            <button
              onClick={handleAddInfo}
              className="btn"
              disabled={!categorySelected || !info.trim()}
            >
              Add {category_name}
            </button>
          </div>
        </div>

        {isCategoryMenuOpen && (
          <div className="category-menu-overlay">
            <div className="category-menu-container">
              <div className="category-menu-header">
                <h3>Select Category</h3>
                <button
                  className="close-menu-btn"
                  onClick={handleCloseCategoryMenu}
                >
                  ×
                </button>
              </div>

              <div className="category-menu-content">
                {categorySet.size > 0 ? (
                  <table className="category-table">
                    <thead>
                      <tr>
                        <th>Available {category_name}</th>
                        <th>Action</th>
                      </tr>
                    </thead>
                    <tbody>
                      {Array.from(categorySet).map((category) => (
                        <tr
                          key={category}
                          className={
                            categorySelected === category ? "selected-row" : ""
                          }
                        >
                          <td className="category-name">{category}</td>
                          <td>
                            <button
                              className="select-category-btn"
                              onClick={() => handleChangCategory(category)}
                            >
                              {categorySelected === category
                                ? "Selected"
                                : "Select"}
                            </button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="no-categories">
                    No {category_name} available
                  </p>
                )}

                <div className="add-new-category-section">
                  <button
                    className="add-new-category-btn"
                    onClick={handleNewCategory}
                  >
                    + Add New {category_name}
                  </button>
                </div>
              </div>

              <div className="category-menu-footer">
                <button
                  className="cancel-btn"
                  onClick={handleCloseCategoryMenu}
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  } else {
    return (
      <div className="add-container">
        <div className="input-section">
          <div className="input">
            <input
              type="text"
              placeholder={`Enter ${category_name}`}
              value={info}
              onChange={(e) => setInfo(e.target.value)}
              onKeyDown={handleKeyDown}
              className="field"
            />
            <button
              onClick={handleAddInfo}
              className="btn"
              disabled={!info.trim()}
            >
              Add {category_name}
            </button>
          </div>
        </div>
      </div>
    );
  }
};

export default AddInfo;