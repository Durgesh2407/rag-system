const express = require("express");
const passport = require("passport");
const {
  registerController,
  loginController,
} = require("../controllers/authController");
const jwt = require("jsonwebtoken");

const router = express.Router();

router.post("/register", registerController);
router.post("/login", loginController);

router.get(
  "/google",
  passport.authenticate("google", {
    scope: ["profile", "email"],
  }),
);

router.get(
  "/google/callback",
  passport.authenticate("google", {
    session: false,
  }),

  async (req, res) => {
    try {
      const token = jwt.sign(
        {
          id: req.user._id,
          email: req.user.email,
        },

        process.env.JWT_key,

        {
          expiresIn: "7d",
        },
      );

      res.cookie("token", token, {
        httpOnly: true,
        secure: false,
        sameSite: "strict",

        maxAge: 7 * 24 * 60 * 60 * 1000,
      });

      res.status(200).json({
        success: true,
        message: "Google login successful",

        token,

        user: req.user,
      });
    } catch (error) {
      console.log(error);

      res.status(500).json({
        success: false,
        message: "OAuth login failed",
      });
    }
  },
);

module.exports = router;
