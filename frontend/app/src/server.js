import sirv from "sirv";
import compression from "compression";
import express from "express";
import session from "express-session";
import bodyParser from "body-parser";
import sessionFileStore from "session-file-store";
import * as sapper from "@sapper/server";

const FileStore = sessionFileStore(session);

const { PORT, NODE_ENV } = process.env;
const dev = NODE_ENV === "development";

const app = express();

const sess = {
    secret: "super-random-secret-here",
    cookie: {
        maxAxe: 31536000,
    },
    resave: false,
    saveUninitialized: true,
    store: new FileStore({
        path: process.env.NOW ? `/tmp/sessions` : `.sessions`,
    }),
};

if (app.get("env") === "production") {
    app.set("trust proxy", 1);
    sess.cookie.secure = true;
}

app.use(bodyParser.json())
    .use(session(sess))
    .use(
        compression({ threshold: 0 }),
        sirv("static", { dev }),
        sapper.middleware({})
    )
    .listen(PORT, err => {
        if (err) console.log("error", err);
    });
