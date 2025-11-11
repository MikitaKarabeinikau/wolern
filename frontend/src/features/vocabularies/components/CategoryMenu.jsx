import React from "react";

function CategoryMenu({
  categorySet,
  categorySelected,
  category_name,
  onCategorySelect,
  onAddCategory,
  onCloseMenu,
}) {
  const handleNewCategory = () => {
    const newCategory = prompt(`Enter new ${category_name}:`);
    if (newCategory && newCategory.trim()) {
      const trimmedCategory = newCategory.trim();
      if (!categorySet.has(trimmedCategory)) {
        onAddCategory(trimmedCategory);
      } else {
        alert(`This ${category_name} already exists!`);
      }
    }
  };

  return (
    <div className="category-menu-overlay">
      <div className="category-menu-container">
        <div className="category-menu-header">
          <h3>Select {category_name}</h3>
          <button className="close-menu-btn" onClick={onCloseMenu}>
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
                        onClick={() => onCategorySelect(category)}
                      >
                        {categorySelected === category ? "Selected" : "Select"}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="no-categories">No {category_name} available</p>
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
          <button className="cancel-btn" onClick={onCloseMenu}>
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}

export default CategoryMenu;
