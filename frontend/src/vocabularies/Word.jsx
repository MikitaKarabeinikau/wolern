import React from 'react';
import Collapsible from './Collapsible'; // Import the component we just made


function Word({ wordData }) {
  // Destructure the data for easier access
  const { word } = wordData;

  return (
 
    <Collapsible title={word}>


        <div>
          <h4>Definitions</h4>
        </div>
        <div>
          <h4>Examples</h4>
        </div>

    </Collapsible>
  );
}

export default Word;