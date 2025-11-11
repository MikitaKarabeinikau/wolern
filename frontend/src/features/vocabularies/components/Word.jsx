import Collapsible from "./Collapsible";
import "../../../../styles/Vocabulary.css";
import "./notification.css"; // Import the notification styles
import UnitCell from "./UnitCell";
import CollapsibleInfo from "./CollapsibleInfo";
import AddInfo from "./AddInfo";
import { groupDataByCategory } from "../../../utils/wordProcessing";
import { useMemo, useState } from "react";
import { useWordApi } from "../hooks/useWordApi";

const defaultVocabularies = ["known", "new", "learning", "strange"];

function Word({
  wordData,
  translations,
  definitions,
  examples,
  synonyms,
  warnings,
  tags,
  onDataChange,
  getToken,
  vocabularies,
}) {
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [loading, setLoading] = useState(null);

  const { addItem, updateItem, deleteItem } = useWordApi(onDataChange);
  const { word } = wordData;

  const vocabularySet = useMemo(() => {
    const uniqueVocabularies = new Set(vocabularies || []);
    return new Set([...defaultVocabularies, ...uniqueVocabularies]);
  }, [vocabularies]);

  const translationsByLanguage = useMemo(
    () => groupDataByCategory(translations, "language"),
    [translations]
  );

  const definitionsByPartOfSpeech = useMemo(
    () => groupDataByCategory(definitions, "part_of_speech"),
    [definitions]
  );

  const examplesByPartOfSpeech = useMemo(
    () => groupDataByCategory(examples, "part_of_speech"),
    [examples]
  );

  // Helper function to show error
  const showError = (errorMsg) => {
    setError(errorMsg);
    setTimeout(() => setError(null), 5000);
  };

  // Helper function to show success message
  const showSuccess = (successMsg) => {
    setSuccessMessage(successMsg);
    setTimeout(() => setSuccessMessage(null), 3000);
  };

  // Helper function to handle async operations
  const handleAsyncOperation = async (operation, operationType) => {
    try {
      setLoading(operationType);
      setError(null);
      await operation();
      showSuccess(`${operationType} successful!`);
    } catch (err) {
      console.error(`Error during ${operationType}:`, err);
      showError(`Failed to ${operationType}: ${err.message}`);
    } finally {
      setLoading(null);
    }
  };

  // Error notification component
  const ErrorNotification = ({ message }) => (
    <div className="error-notification">
      <span>⚠️ {message}</span>
      <button className="close-button" onClick={() => setError(null)}>
        ✕
      </button>
    </div>
  );

  // Success notification component
  const SuccessNotification = ({ message }) => (
    <div className="success-notification">
      <span>✓ {message}</span>
    </div>
  );

  // Loading spinner component
  const LoadingSpinner = () => (
    <div className="loading-spinner">
      <span>{loading}...</span>
    </div>
  );

  const renderSection = (title, items, categoryName, apiEndpoint, itemKey) => (
    <CollapsibleInfo title={title}>
      {items && items.length > 0 ? (
        <ul>
          {items.map((item) => (
            <UnitCell
              key={item.id}
              item={{ id: item.id, text: item[itemKey] }}
              isLoading={loading === `update-${itemKey}-${item.id}`}
              onUpdate={(id, newText) => {
                if (!newText || newText.trim() === "") {
                  showError(`${categoryName} cannot be empty`);
                  return;
                }
                handleAsyncOperation(
                  () =>
                    updateItem(`${apiEndpoint}/${id}`, { [itemKey]: newText }),
                  `Update ${categoryName}`
                );
              }}
              onDelete={(id) => {
                if (
                  window.confirm(
                    `Are you sure you want to delete this ${categoryName.toLowerCase()}?`
                  )
                ) {
                  handleAsyncOperation(
                    () => deleteItem(`${apiEndpoint}/${id}`),
                    `Delete ${categoryName}`
                  );
                }
              }}
            />
          ))}
        </ul>
      ) : (
        <p>No {title.toLowerCase()} available.</p>
      )}
      <AddInfo
        withCategory={false}
        category_name={categoryName}
        isLoading={loading === `add-${itemKey}`}
        onAddInfo={(_, newItem) => {
          if (!newItem || newItem.trim() === "") {
            showError(`${categoryName} cannot be empty`);
            return;
          }
          handleAsyncOperation(
            () =>
              addItem(apiEndpoint, {
                word_id: wordData.id,
                [itemKey]: newItem,
              }),
            `Add ${categoryName}`
          );
        }}
      />
    </CollapsibleInfo>
  );

  return (
    <div>
      {/* Notification Container */}
      <div className="notification-container">
        {error && <ErrorNotification message={error} />}
        {successMessage && <SuccessNotification message={successMessage} />}
        {loading && <LoadingSpinner />}
      </div>

      <Collapsible
        title={wordData.word}
        wordId={wordData.id}
        onDelete={() => {
          if (
            window.confirm(
              "Are you sure you want to delete this word? This action cannot be undone."
            )
          ) {
            handleAsyncOperation(
              () =>
                deleteItem(`http://localhost:8000/user/words/${wordData.id}`),
              "Delete word"
            );
          }
        }}
        onChangeVocabulary={(word_id, newVocabulary) => {
          console.log("Changing vocabulary for word ID:", word_id);
          console.log("New Vocabulary:", newVocabulary);
          handleAsyncOperation(
            () =>
              updateItem(
                `http://localhost:8000/words/vocabulary/${newVocabulary}/${word_id}`,
                {}
              ),
            "Change vocabulary"
          );
        }}
        vocabularies={vocabularySet}
        currentSelectedVocabulary={wordData.vocabulary}
      >
        {/* Rest of the component remains the same... */}
        {/* Translations Section */}
        <CollapsibleInfo title="Translations">
          {Object.keys(translationsByLanguage).length > 0 ? (
            Object.keys(translationsByLanguage).map((language) => (
              <div key={language}>
                <strong>{language}:</strong>
                <ul>
                  {translationsByLanguage[language].map((trans) => (
                    <UnitCell
                      key={trans.id}
                      item={{ id: trans.id, text: trans.translation }}
                      isLoading={loading === `update-translation-${trans.id}`}
                      onUpdate={(id, newText) => {
                        if (!newText || newText.trim() === "") {
                          showError("Translation cannot be empty");
                          return;
                        }
                        handleAsyncOperation(
                          () =>
                            updateItem(
                              `http://localhost:8000/user/words/translations/${id}`,
                              { translation: newText }
                            ),
                          "Update translation"
                        );
                      }}
                      onDelete={(id) => {
                        if (
                          window.confirm(
                            "Are you sure you want to delete this translation?"
                          )
                        ) {
                          handleAsyncOperation(
                            () =>
                              deleteItem(
                                `http://localhost:8000/user/words/translations/${id}`
                              ),
                            "Delete translation"
                          );
                        }
                      }}
                    />
                  ))}
                </ul>
              </div>
            ))
          ) : (
            <p>No translations available.</p>
          )}
          <AddInfo
            withCategory={true}
            category_name="Language"
            categories={Array.from(
              new Set(translations.map((t) => t.language))
            )}
            isLoading={loading === "add-translation"}
            onAddInfo={(language, newTranslation) => {
              if (
                !language ||
                !newTranslation ||
                newTranslation.trim() === ""
              ) {
                showError("Language and translation cannot be empty");
                return;
              }
              handleAsyncOperation(
                () =>
                  addItem(
                    `http://localhost:8000/user/words/${wordData.id}/${language}/translations/${newTranslation}`,
                    {
                      word_id: wordData.id,
                      language,
                      translation: newTranslation,
                    }
                  ),
                "Add translation"
              );
            }}
          />
        </CollapsibleInfo>

        {/* Definitions Section */}
        <CollapsibleInfo title="Definitions">
          {Object.keys(definitionsByPartOfSpeech).length > 0 ? (
            Object.keys(definitionsByPartOfSpeech).map((partOfSpeech) => (
              <div key={partOfSpeech}>
                <strong>{partOfSpeech}:</strong>
                <ul>
                  {definitionsByPartOfSpeech[partOfSpeech].map((def) => (
                    <UnitCell
                      key={def.id}
                      item={{ id: def.id, text: def.definition }}
                      isLoading={loading === `update-definition-${def.id}`}
                      onUpdate={(id, newText) => {
                        if (!newText || newText.trim() === "") {
                          showError("Definition cannot be empty");
                          return;
                        }
                        handleAsyncOperation(
                          () =>
                            updateItem(
                              `http://localhost:8000/user/words/definitions/${id}`,
                              {
                                definition: newText,
                                part_of_speech: partOfSpeech,
                              }
                            ),
                          "Update definition"
                        );
                      }}
                      onDelete={(id) => {
                        if (
                          window.confirm(
                            "Are you sure you want to delete this definition?"
                          )
                        ) {
                          handleAsyncOperation(
                            () =>
                              deleteItem(
                                `http://localhost:8000/user/words/definitions/${id}`
                              ),
                            "Delete definition"
                          );
                        }
                      }}
                    />
                  ))}
                </ul>
              </div>
            ))
          ) : (
            <p>No definitions available.</p>
          )}
          <AddInfo
            withCategory={true}
            category_name="Part of Speech"
            categories={Array.from(
              new Set(definitions.map((d) => d.part_of_speech))
            )}
            isLoading={loading === "add-definition"}
            onAddInfo={(partOfSpeech, newDefinition) => {
              if (
                !partOfSpeech ||
                !newDefinition ||
                newDefinition.trim() === ""
              ) {
                showError("Part of speech and definition cannot be empty");
                return;
              }
              handleAsyncOperation(
                () =>
                  addItem(
                    `http://localhost:8000/user/words/definitions/${wordData.id}`,
                    {
                      word_id: wordData.id,
                      part_of_speech: partOfSpeech,
                      definition: newDefinition,
                    }
                  ),
                "Add definition"
              );
            }}
          />
        </CollapsibleInfo>

        {/* Examples Section */}
        <CollapsibleInfo title="Examples">
          {Object.keys(examplesByPartOfSpeech).length > 0 ? (
            Object.keys(examplesByPartOfSpeech).map((partOfSpeech) => (
              <div key={partOfSpeech}>
                <strong>{partOfSpeech}:</strong>
                <ul>
                  {examplesByPartOfSpeech[partOfSpeech].map((ex) => (
                    <UnitCell
                      key={ex.id}
                      item={{ id: ex.id, text: ex.example_sentence }}
                      isLoading={loading === `update-example-${ex.id}`}
                      onUpdate={(id, newText) => {
                        if (!newText || newText.trim() === "") {
                          showError("Example cannot be empty");
                          return;
                        }
                        handleAsyncOperation(
                          () =>
                            updateItem(
                              `http://localhost:8000/user/words/examples/${id}`,
                              { example_sentence: newText }
                            ),
                          "Update example"
                        );
                      }}
                      onDelete={(id) => {
                        if (
                          window.confirm(
                            "Are you sure you want to delete this example?"
                          )
                        ) {
                          handleAsyncOperation(
                            () =>
                              deleteItem(
                                `http://localhost:8000/user/words/examples/${id}`
                              ),
                            "Delete example"
                          );
                        }
                      }}
                    />
                  ))}
                </ul>
              </div>
            ))
          ) : (
            <p>No examples available.</p>
          )}
          <AddInfo
            withCategory={true}
            category_name="Part of Speech"
            categories={Array.from(
              new Set(examples.map((e) => e.part_of_speech))
            )}
            isLoading={loading === "add-example"}
            onAddInfo={(partOfSpeech, newExample) => {
              if (!partOfSpeech || !newExample || newExample.trim() === "") {
                showError("Part of speech and example cannot be empty");
                return;
              }
              handleAsyncOperation(
                () =>
                  addItem(
                    `http://localhost:8000/user/words/examples/${wordData.id}`,
                    {
                      word_id: wordData.id,
                      part_of_speech: partOfSpeech,
                      example_sentence: newExample,
                    }
                  ),
                "Add example"
              );
            }}
          />
        </CollapsibleInfo>

        {/* Synonyms Section */}
        {renderSection(
          "Synonyms",
          synonyms,
          "Synonym",
          "http://localhost:8000/user/words/synonyms",
          "synonym"
        )}

        {/* Tags Section */}
        {renderSection(
          "Tags",
          tags,
          "Tag",
          "http://localhost:8000/user/words/tags",
          "tag"
        )}

        {/* Warnings Section */}
        {renderSection(
          "Warnings",
          warnings,
          "Warning",
          "http://localhost:8000/user/words/warnings",
          "warning"
        )}
      </Collapsible>
    </div>
  );
}

export default Word;
