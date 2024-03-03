const express = require("express");
const items = require("./data/items.json");
const path = require("path");

const actives = [...items.items].filter((item) => item.type === "active");
const passives = [...items.items].filter((item) => item.type === "passive");

const app = express();
const PORT = 8080;
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  next();
});

app.use("/images", express.static(path.join(__dirname, "images")));

app.get("/api/boss/:name/original", (req, res) => {
  const bossName = req.params.name + ".png";

  const image = path.join(__dirname, "images/original", bossName);

  if (require("fs").existsSync(image)) {
    res.sendFile(image);
  } else {
    res.status(404).send("Image not found");
  }
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
