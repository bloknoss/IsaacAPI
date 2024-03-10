const express = require("express");
const items = require("./data/items.json");
const path = require("path");
const fs = require("fs");

const actives = [...items.items].filter((item) => item.type === "active");
const passives = [...items.items].filter((item) => item.type === "passive");

const app = express();
const PORT = 8080;
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.use("/images", express.static(path.join(__dirname, "images")));

function readFilesSync(dir) {
  const files = [];

  fs.readdirSync(dir).forEach((filename) => {
    const name = path.parse(filename).name;
    const ext = path.parse(filename).ext;
    const filepath = `${dir.split(__dirname)[1].replaceAll("\\","/")}/${filename}`;

    files.push({ filepath, name, ext });
  });

  files.sort((a, b) => {
    // natural sort alphanumeric strings
    // https://stackoverflow.com/a/38641281
    return a.name.localeCompare(b.name, undefined, { numeric: true, sensitivity: "base" });
  });

  return files;
}

function renameKeys(obj, newKeys) {
  const myObject = obj;

  // Renaming the key from 'oldKey' to 'newKey'
  const { oldKey: newKey, ...rest } = myObject;
  const updatedObject = { newKey, ...rest };

  console.log(updatedObject); // { newKey: 'value' }
  return updatedObject;
}

app.get("/api/bosses/", (req, res) => {
  const originalBosses = path.join(__dirname, "images/original");
  const silhouetteBosses = path.join(__dirname, "images/silhouette");

  const bosses = readFilesSync(originalBosses);
  const silhouette = readFilesSync(silhouetteBosses);

  res.json({ original: bosses, silhouette: silhouette });
});

app.get("/api/boss/:name/original", (req, res) => {
  const bossName = req.params.name + ".png";

  const image = path.join(__dirname, "images/original", bossName);
  const json = { bossName: image };
});

app.get("/api/boss/:name/hidden", (req, res) => {
  const bossName = req.params.name + ".png";

  const image = path.join(__dirname, "images/silhouette", bossName);

  if (require("fs").existsSync(image)) {
    res.sendFile(image);
  } else {
    res.status(404).send("Image not found");
  }
});

app.get("/api/items/query/:name", (req, res) => {
  let name = req.params.name;

  items.items.forEach((item) => {
    if (item !== null && item.name.toLowerCase() === name.toLowerCase()) {
      res.json(item);
    }
  });

  res.json({ message: "Item not found" });
  res.status(200);
});

app.get("/api/items/passives", (req, res) => {
  res.json(passives);
});

app.get("/api/items/actives", (req, res) => {
  res.json(actives);
});

app.get("/api/items/", (req, res) => {
  res.json(items.items);
});

app.get("/api/items/:id", (req, res) => {
  res.json(items.items[req.params.id]);
});

app.get("/api/items/passives/:id", (req, res) => {
  res.json(passives[req.params.id]);
});

app.get("/api/items/actives/:id", (req, res) => {
  res.json(actives[req.params.id]);
});

app.listen(PORT, () => {
  console.clear();
  console.log(`API REST Listening on port ${PORT}`);
});
