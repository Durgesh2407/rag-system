const passport = require("passport");
const GoogleStrategy = require("passport-google-oauth20").Strategy;
const User = require("../models/userModel");


passport.use(
  new GoogleStrategy(
    {
      clientID: process.env.GOOGLE_CLIENT_ID,

      clientSecret: process.env.GOOGLE_CLIENT_SECRET,

      callbackURL: "http://localhost:8080/api/v1/auth/google/callback",
    },

    async (accessToken, refreshToken, profile, done) => {
      try {
        let user = await User.findOne({
          email: profile.emails[0].value,
        });

        if (!user) {
          user = await User.create({
            username: profile.displayName,

            email: profile.emails[0].value,

            googleId: profile.id,

            authProvider: "google",
          });
        }

        return done(null, user);
      } catch (error) {
        return done(error, null);
      }
    },
  ),
);

module.exports = passport;
