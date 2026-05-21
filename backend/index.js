const express = require("express");
const morgan = require("morgan");
const cors = require("cors");
const colors = require("colors");
const dotenv = require("dotenv");
const { connectDB } = require("./config/db");
const bodyParser = require("body-parser");
const cookieParser = require("cookie-parser");

dotenv.config();

const passport = require("./config/passport");
const AuthRoutes = require("./routes/authRouter");

const app = express();

connectDB();

app.use(passport.initialize());
app.use(
  cors({
    origin: "http://localhost:5173",
    credentials: true,
  }),
);
app.use(cookieParser());
app.use(morgan("dev"));
app.use(express.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use("/api/v1/auth", AuthRoutes);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(` Server is running on port ${PORT} `.bgBlue.white);
});
