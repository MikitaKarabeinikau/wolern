import React, { useState, useCallback, useMemo } from "react";
import CategoryMenu from "./CategoryMenu";
import "../../../../styles/Vocabulary.css";

const AddInfo = ({
  withCategory,
  category_name,
  categories = [],
  onAddInfo,
  onAddCategory,
  isLoading = false,
}) => {
  const [categorySet, setCategorySet] = useState(new Set(categories || []));
  const [info, setInfo] = useState("");
  const [isCategoryMenuOpen, setIsCategoryMenuOpen] = useState(false);
  const [categorySelected, setCategorySelected] = useState(categories[0] || "");

  const handleToggleCategoryMenu = useCallback(() => {
    setIsCategoryMenuOpen((prev) => !prev);
  }, []);

  const handleCategorySelect = useCallback((newCategory) => {
    setCategorySelected(newCategory);
    setIsCategoryMenuOpen(false);
  }, []);

  const handleAddCategory = useCallback(
    (newCategory) => {
      if (!categorySet.has(newCategory)) {
        const updatedCategories = new Set([...categorySet, newCategory]);
        setCategorySet(updatedCategories);
        setCategorySelected(newCategory);
        if (onAddCategory) {
          onAddCategory(newCategory);
        }
      } else {
        alert(`This ${category_name} already exists!`);
      }
    },
    [categorySet, onAddCategory, category_name]
  );

  const handleAddInfo = useCallback(() => {
    if (withCategory && !categorySelected.trim()) {
      alert(`Please select a ${category_name}`);
      return;
    }
    if (!info.trim()) {
      alert(`Please enter a valid ${category_name}`);
      return;
    }
    onAddInfo(categorySelected, info);
    setInfo("");
  }, [withCategory, categorySelected, info, category_name, onAddInfo]);

  const handleKeyDown = useCallback(
    (e) => {
      if (e.key === "Enter") {
        handleAddInfo();
      }
    },
    [handleAddInfo]
  );

  return (
    <div className="add-container">
      <div className="input-section">
        {withCategory && (
          <div className="category-selector">
            <label>
              Category: <strong>{categorySelected || "None"}</strong>
            </label>
            <button
              className="change-category-btn"
              onClick={handleToggleCategoryMenu}
              disabled={isLoading} // Add disabled state
            >
              {isCategoryMenuOpen ? "Close Menu" : `Change ${category_name}`}
            </button>
          </div>
        )}

        <div className="input">
          <input
            type="text"
            placeholder={`Enter ${category_name}`}
            value={info}
            onChange={(e) => setInfo(e.target.value)}
            onKeyDown={handleKeyDown}
            className="field"
            disabled={isLoading} // Add disabled state
          />
          <button
            onClick={handleAddInfo}
            className="btn"
            disabled={
              isLoading || // Add loading check
              (withCategory ? !categorySelected || !info.trim() : !info.trim())
            }
          >
            {isLoading ? "Adding..." : `Add ${category_name}`}
          </button>
        </div>
      </div>

      {isCategoryMenuOpen && withCategory && (
        <CategoryMenu
          categorySet={categorySet}
          categorySelected={categorySelected}
          category_name={category_name}
          onCategorySelect={handleCategorySelect}
          onAddCategory={handleAddCategory}
          onCloseMenu={handleToggleCategoryMenu}
        />
      )}
    </div>
  );
};

export default AddInfo;
