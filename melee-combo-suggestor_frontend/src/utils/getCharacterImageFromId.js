import characterImages from '../characterImages';// Adjust the path as necessary
import { characterIdsFromCombosTable } from '../gameIds'; // Adjust the path as necessary

export const getCharacterImageFromId = (characterId, imageType = 'stockIcon') => {
  // Convert the character ID to the character name, ensuring it's in lower case and matches the keys in characterImages
  const characterKey = characterIdsFromCombosTable[characterId]?.toLowerCase().replace(/\s/g, '');

  // Return the requested image type if available, otherwise a default image path
  return characterImages[characterKey]?.[imageType] || '/defaultCharacterIcon.png';
};
