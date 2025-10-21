import React from 'react'; // Removed unused useState, useEffect
import Collapsible from './Collapsible';
import '../../styles/Word.css';
import UnitCell from './UnitCell';
import CollapsibleInfo from './CollapsibleInfo';

const defaultVocabularies = ['known', 'unknown', 'learning', 'strange']; // Define default vocabularies


function Word({ wordData, translations, definitions, examples, synonyms, warnings, tags, onDataChange, getToken }) {
  const { word } = wordData;


  const translationsByLanguage = (translations || []).reduce((acc, trans) => {
    const lang = trans.language || 'Unknown';
    if (!acc[lang]) {
      acc[lang] = [];
    }
    acc[lang].push(trans);
    return acc;
  }, {});

  const definitionsByPartOfLanguage = (definitions || []).reduce((acc, def) => {
    const pos = def.part_of_speech || 'Unknown';
    if (!acc[pos]) {
      acc[pos] = [];
    }
    acc[pos].push(def);
    return acc;
  }, {});

  const examplesByPartOfLanguage = (examples || []).reduce((acc, ex) => {
    const pos = ex.part_of_speech || 'Unknown';
    if (!acc[pos]) {
      acc[pos] = [];
    }
    acc[pos].push(ex);
    return acc;
  }, {});

  return (
    <Collapsible title={word}
    wordId = {wordData.id}
      onDelete={async (id) => {
        try{
          const token = await getToken();
          const response = await fetch(`http://localhost:8000/user/words/${id}`, {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
          });
          if (response.ok) {
            console.log(`Word ${id} deleted successfully`);
            onDataChange(); // Notify parent to refresh data
          } else {
            console.error('Failed to delete word');
          }
        } catch (error) {
          console.error('Error deleting word:', error);
        }
      }}
      onChangeVocabulary={async (id, new_vocabulary) => {
        try {
          const token = await getToken();
          const response = await fetch(`http://localhost:8000/words/vocabulary/${new_vocabulary}/${id}`, { // Corrected URL
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.ok) {
            console.log(`Change Vocabulary for Word ${id} successfully`);
            onDataChange(); // Notify parent to refresh data
          } else {
            console.error('Failed to change vocabulary for word');
          }
        } catch (error) {
          console.error('Error changing vocabulary:', error);
        }
      }}
      vocabularies = {defaultVocabularies}

      >
      
      {/* Translations Section */}
      <CollapsibleInfo title="Translations">
        {/* This correctly checks if there are any translations to display */}
        {Object.keys(translationsByLanguage).length > 0 ? (
          // This maps over each language (e.g., "Spanish", "French")
          Object.keys(translationsByLanguage).map(language => (
            <div key={language}>
              <strong>{language}:</strong>
              <ul>
                {translationsByLanguage[language].map(trans => (
                  <UnitCell
                    key={trans.id}
                    item={{ id: trans.id, text: trans.translation }}
                    onUpdate={async (id, newText) => {
                      try {
                        const token = await getToken();
                        const response = await fetch(`http://localhost:8000/user/words/translations/${id}`, {
                          method: 'PUT',
                          headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${token}`,
                          },
                          body: JSON.stringify({ translation: newText }), // Adjust payload as needed
                        });
                        if (response.ok) {
                          console.log(`Translation ${id} updated successfully`);
                          onDataChange(); // Notify parent to refresh data
                        } else {
                          console.error('Failed to update translation');
                        }
                      } catch (error) {
                        console.error('Error updating translation:', error);
                      }
                      console.log(`Update ${id} with new text: ${newText}`);
                    }}
                    onDelete={async (id) => {
                      console.log(`Delete button clicked for translation ID: ${id}`);
                      try {
                        const token = await getToken();
                        const response = await fetch(`http://localhost:8000/user/words/translations/${id}`, {
                          method: 'DELETE',
                          headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${token}`,
                          },
                        });
                        if (response.ok) {
                          console.log(`Translation ${id} deleted successfully`);
                          onDataChange(); // Notify parent to refresh data
                        } else {
                          console.error('Failed to delete translation');
                        }
                      } catch (error) {
                        console.error('Error deleting translation:', error);
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
      </CollapsibleInfo>
      <CollapsibleInfo title="Definitions">
        {Object.keys(definitionsByPartOfLanguage).length > 0 ? (
          Object.keys(definitionsByPartOfLanguage).map(pos => (
            
            <div key={pos}>
              <strong>{pos}:</strong>
              {definitionsByPartOfLanguage[pos].map(def => (
               <UnitCell
                    key={def.id}
                    item={{ id: def.id, text: def.definition }}
                    onUpdate={async (id, newText) => {
                      try{
                        const token = await getToken();
                        const response = await fetch(`http://localhost:8000/user/words/definitions/${id}`, {
                          method: 'PUT',
                          headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${token}`,
                          },
                          body: JSON.stringify({ definition: newText }), // Adjust payload as needed
                        });
                        if (response.ok) {
                          console.log(`Definition ${id} updated successfully`);
                          onDataChange(); // Notify parent to refresh data
                        } else {
                          console.error('Failed to update definition');
                        }
                      } catch (error) {
                        console.error('Error updating definition:', error);
                      }
                        console.log(`Update ${id} with new text: ${newText}`);
                    }}
                    onDelete={async (id) => {
                      console.log(`Delete button clicked for definition ID: ${id}`);
                      try {
                        const token = await getToken();
                        const response = await fetch(`http://localhost:8000/user/words/definitions/${id}`, {
                          method: 'DELETE',
                          headers: {
                            'Content-Type': 'application/json',
                            Authorization: `Bearer ${token}`,
                          },
                        });
                        if (response.ok) {
                          console.log(`Definition ${id} deleted successfully`);
                          onDataChange(); // Notify parent to refresh data
                        } else {
                          console.error('Failed to delete definition');
                        } 
                      } catch (error) {
                        console.error('Error deleting definition:', error);
                      }
                    }}
                  />
              ))}
            </div>
          ))
        ) : (
          <p>No definitions available.</p>
        )}
      </CollapsibleInfo>
        <CollapsibleInfo title="Examples">
         {Object.keys(examplesByPartOfLanguage).length > 0 ? (
          Object.keys(examplesByPartOfLanguage).map(pos => (
            
            <div key={pos}>
              <strong>{pos}:</strong>
              {examplesByPartOfLanguage[pos].map(example => (
                <UnitCell
                    key={example.id}
                    item={{ id: example.id, text: example.example_sentence }}
                    onUpdate={async (id, newText) => {
                      try {
                        const token = await getToken();
                        const response = await fetch(
                          `http://localhost:8000/user/words/examples/${id}`,
                          {
                            method: "PUT",
                            headers: {
                              "Content-Type": "application/json",
                              Authorization: `Bearer ${token}`,
                            },
                            body: JSON.stringify({ example_sentence: newText }),
                          }
                        );
                        if (response.ok) {
                          console.log(`Example ${id} updated successfully`);
                          onDataChange(); // Notify parent to refresh data
                        } else {
                          console.error("Failed to update example");
                        }
                      } catch (error) {
                        console.error("Error updating example:", error);
                      }
                      console.log(`Update ${id} with new text: ${newText}`);
                    }}
                    onDelete={async (id) => {
                      console.log(`Delete button clicked for example ID: ${id}`);
                      try {
                        const token = await getToken();
                        const response = await fetch(`http://localhost:8000/user/words/examples/${id}`, {
                          method: "DELETE",
                          headers: {
                            "Content-Type": "application/json",
                            Authorization: `Bearer ${token}`,
                          },
                        });
                        if (response.ok) {
                          console.log(`Definition ${id} deleted successfully`);
                          onDataChange(); // Notify parent to refresh data
                        } else {
                          console.error("Failed to delete definition");
                        }
                      } catch (error) {
                        console.error("Error deleting definition:", error);
                      }
                    }}
                  />
              ))}
            </div>
          ))
        ) : (
          <p>No definitions available.</p>
        )}
      </CollapsibleInfo>
      <CollapsibleInfo title="Synonyms">
        {synonyms && synonyms.length > 0 ? (
          <ul>
            {synonyms.map(syn => (
              <UnitCell 
                key={syn.id}
                item={{ id: syn.id, text: syn.synonym }}
                onUpdate={async (id, newText) => {
                  try {
                    const token = await getToken();
                    const response = await fetch(`http://localhost:8000/user/words/synonyms/${id}`, {
                      method: 'PUT',
                      headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                      },
                      body: JSON.stringify({ synonym: newText }), // Adjust payload as needed
                    });
                    if (response.ok) {
                      console.log(`Synonym ${id} updated successfully`);
                      onDataChange(); // Notify parent to refresh data
                    } else {
                      console.error('Failed to update synonym');
                    }
                  } catch (error) {
                    console.error('Error updating synonym:', error);
                  }
                  console.log(`Update ${id} with new text: ${newText}`);
                }}
                onDelete={async (id) => {
                  try {
                    const token = await getToken();
                    const response = await fetch(`http://localhost:8000/user/words/synonyms/${id}`, {
                      method: 'DELETE',
                      headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                      },
                    });
                    if (response.ok) {
                      console.log(`Synonym ${id} deleted successfully`);
                      onDataChange(); // Notify parent to refresh data
                    } else {
                      console.error('Failed to delete synonym');
                    }
                  } catch (error) {
                    console.error('Error deleting synonym:', error);
                  }
                }}
              />
            ))}
          </ul>
        ) : (
          <p>No synonyms available.</p>
        )}
      </CollapsibleInfo>
      <CollapsibleInfo title="Tags">

        {tags && tags.length > 0 ? (
          <ul>
            {tags.map(tag => (
              <UnitCell 
                key={tag.id}
                item={{ id: tag.id, text: tag.tag }}
                onUpdate={async (id, newText) => {
                  try {
                    const token = await getToken();
                    const response = await fetch(`http://localhost:8000/user/words/tags/${id}`, {
                      method: 'PUT',
                      headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                      },
                      body: JSON.stringify({ tag: newText }), // Adjust payload as needed
                    });
                    if (response.ok) {
                      console.log(`Tag ${id} updated successfully`);
                      onDataChange(); // Notify parent to refresh data
                    } else {
                      console.error('Failed to update tag');
                    }
                  } catch (error) {
                    console.error('Error updating tag:', error);
                  }
                  console.log(`Update ${id} with new text: ${newText}`);
                }}
                onDelete={async (id) => {
                  try {
                    const token = await getToken();
                    const response = await fetch(`http://localhost:8000/user/words/tags/${id}`, {
                      method: 'DELETE',
                      headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                      },
                    });
                    if (response.ok) {
                      console.log(`Tag ${id} deleted successfully`);
                      onDataChange(); // Notify parent to refresh data
                    } else {
                      console.error('Failed to delete tag');
                    }
                  } catch (error) {
                    console.error('Error deleting tag:', error);
                  }
                }}
              />
            ))}
          </ul>
        ) : (
          <p>No tags available.</p>
        )}  
      </CollapsibleInfo>
      <CollapsibleInfo title="Warnings">
        {warnings && warnings.length > 0 ? (
          <ul>
            {warnings.map(warn => (
              <UnitCell 
                key={warn.id}
                  item={{ id: warn.id, text: warn.warning }}
                  onUpdate={async (id, newText) => {
                    try {
                      const token = await getToken();
                      const response = await fetch(`http://localhost:8000/user/words/warnings/${id}`, {
                        method: 'PUT',
                        headers: {
                          'Content-Type': 'application/json',
                          Authorization: `Bearer ${token}`,
                        },
                        body: JSON.stringify({ warning: newText }), // Adjust payload as needed
                      });
                      if (response.ok) {
                        console.log(`Warning ${id} updated successfully`);
                        onDataChange(); // Notify parent to refresh data
                      } else {
                        console.error('Failed to update warning');
                      }
                    } catch (error) {
                      console.error('Error updating warning:', error);
                    }
                  }}
                onDelete={async (id) => {
                  try {
                    const token = await getToken();
                    const response = await fetch(`http://localhost:8000/user/words/warnings/${id}`, {
                      method: 'DELETE',
                      headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`,
                      },
                    });
                    if (response.ok) {
                      console.log(`Warning ${id} deleted successfully`);
                      onDataChange(); // Notify parent to refresh data
                    } else {
                      console.error('Failed to delete warning');
                    }
                  } catch (error) {
                    console.error('Error deleting warning:', error);
                  }
                }}
              />
            ))}
          </ul>
        ) : (
          <p>No warnings available.</p>
        )}
      </CollapsibleInfo>
    </Collapsible>
  );
}

export default Word;