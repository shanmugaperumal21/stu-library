// MongoDB Atlas public app settings. The connection URI stays on the server.
const envUri = (typeof process !== 'undefined' && process.env && process.env.MONGODB_URI)
  ? process.env.MONGODB_URI
  : "";

export const mongoConfig = {
  uri: envUri,
  dbName: "studentsphere_db",
  collectionName: "students"
};

export function getActiveMongoConfig() {
  return mongoConfig;
}

export function isMongoConfigured(config = getActiveMongoConfig()) {
  if (!config) return false;
  const uri = (config.uri || '').trim();
  return Boolean(
    uri &&
    (uri.startsWith('mongodb://') || uri.startsWith('mongodb+srv://')) &&
    !uri.includes('<password>')
  );
}
