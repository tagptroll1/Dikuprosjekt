import sirv from "sirv";
import compression from "compression";
import express from "express";
import session from "express-session";
import bodyParser from "body-parser";
import sessionFileStore from "session-file-store";

import * as sapper from "@sapper/server";
import * as expressWinston from "express-winston";
import * as winston from "winston";

winston.defaults.transports.console.timestamp = true;

const FileStore = sessionFileStore(session);

const { PORT, NODE_ENV } = process.env;

const dev = NODE_ENV === "development";

const app = express();

const ignoredPaths = ["/favicon.png", "/global.css", "/service-worker.js"];


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

// Setup loggers
winston.loggers.add("file-logger", {
    level: "info",
    format: winston.format.json(),
    defaultMeta: { service: "user-service" },
    meta: true,
    transports: [
        new winston.transports.File({ filename: "error.log", level: "error" }),
        new winston.transports.File({ filename: "meta.log" }),
    ],
});

if (dev) {
    winston.loggers.add("dev-logger", {
        format: winston.format.simple(),
        transports: [
            new winston.transports.Console({
                level: "debug",
            }),
        ],
    });
}

app
    .use(
        expressWinston.logger({
            transports: [new winston.transports.Console()],
            format: winston.format.combine(winston.format.colorize(), winston.format.simple()),
            meta: false,
            msg: "HTTP {{res.statusCode}} {{req.method}} {{req.url}} {{res.responseTime}}ms",
            expressFormat: false,
            colorize: true,
            ignoreRoute: ({ path }) => ignoredPaths.includes(path) || path.slice(0, 7) === "/client",
        })
    )
    .use(
        expressWinston.logger({
            level: "info",
            format: winston.format.json(),
            defaultMeta: { service: "user-service" },
            transports: [
                new winston.transports.File({ filename: "error.log", level: "error" }),
                new winston.transports.File({ filename: "meta.log" }),
            ],
            ignoreRoute: ({ path }) => ignoredPaths.includes(path) || path.slice(0, 7) === "/client",
        })
    )
    .use(bodyParser.json())
    .use(session(sess))
    .use(
        compression({ threshold: 0 }),
        sirv("static", { dev }),
        sapper.middleware({})
    )
    .use(expressWinston.errorLogger({
        transports: [
            new winston.transports.Console()
        ],
        format: winston.format.combine(
            winston.format.colorize(),
            winston.format.json()
        )
    }))
    .listen(PORT, err => {
        if (err) console.log("error", err);
    });