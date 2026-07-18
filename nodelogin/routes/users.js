require('dotenv').config();
const express = require('express');
const router = express.Router();
const bcrypt = require('bcryptjs');
const passport = require('passport');
var jwt = require('jsonwebtoken');
const sgMail = require('@sendgrid/mail');
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

// Load User model
const User = require('../models/User');
const { forwardAuthenticated } = require('../config/auth');

// Login Page
router.get('/login', forwardAuthenticated, (req, res) => res.render('login'));

//Password Reset Page
router.get('/reset', forwardAuthenticated, (req, res) => res.render('reset'));

// Register Page
router.get('/register', forwardAuthenticated, (req, res) => res.render('register'));

// Register
router.post('/register', (req, res) => {
	const { name, email, password, password2 } = req.body;
	let errors = [];

	if (!name || !email || !password || !password2) {
		errors.push({ msg: 'Please enter all fields' });
	}

	if (password != password2) {
		errors.push({ msg: 'Passwords do not match' });
	}

	if (password.length < 6) {
		errors.push({ msg: 'Password must be at least 6 characters' });
	}

	if (errors.length > 0) {
		res.render('register', {
			errors,
			name,
			email,
			password,
			password2,
		});
	} else {
		User.findOne({ email: email }).then((user) => {
			if (user) {
				errors.push({ msg: 'Email already exists' });
				res.render('register', {
					errors,
					name,
					email,
					password,
					password2,
				});
			} else {
				bcrypt.genSalt(10, (err, salt) => {
					bcrypt.hash(password, salt, (err, hash) => {
						if (err) throw err;
						console.log(process.env.JWT_SECRET);
						var token = jwt.sign({ name, email, password: hash }, process.env.JWT_SECRET);
						const msg = {
							to: email,
							from: process.env.SENDGRID_EMAIL,
							subject: 'Verification Mail for Fake News Detection',
							text: 'Copy and Paste this url in browser ' + process.env.APP_URL + '/validate/' + token,
							html: `<h2 style="text-align:center;" >Your Verification Link is Below</h2><br/><a href="${
								process.env.APP_URL + '/validate/' + token
							}" >Link</a>`,
						};
						sgMail
							.send(msg)
							.then((data) => {
								req.flash(
									'success_msg',
									`Verification Mail sent to the Email ${email}, Please make sure to check the spam section aswell`
								);
								res.redirect('/users/login');
							})
							.catch((err) => {
								console.log(err);
								req.flash('error_msg', 'Error in sending verfication Mail');
								res.redirect('/users/login');
							});
					});
				});
			}
		});
	}
});

// Login
router.post('/login', (req, res, next) => {
	passport.authenticate('local', {
		successRedirect: '/dashboard',
		failureRedirect: '/users/login',
		failureFlash: true,
	})(req, res, next);
});

//send Reset Link
router.post('/reset', (req, res) => {
	const { email } = req.body;
	if (!email) {
		return res.render('reset', {
			errors: [{ msg: 'Invalid Email address' }],
      email
		});
	}

	User.findOne({ email: email }).then((user) => {
		if (user) {
      var token = jwt.sign({ email }, process.env.JWT_SECRET);
      const msg = {
        to: email,
        from: process.env.SENDGRID_EMAIL,
        subject: 'Password Reset Mail for Fake News Detection',
        text: 'Copy and Paste this url in browser ' + process.env.APP_URL + '/reset/' + token,
        html: `<h2 style="text-align:center;" >Your Reset Password Link is Below</h2><br/><a href="${
          process.env.APP_URL + '/reset/' + token
        }" >Link</a>`,
      };
      sgMail
        .send(msg)
        .then(data => {
          req.flash(
            'success_msg',
            `Reset Password Mail sent to the Email ${email}, Please make sure to check the spam section aswell`
          );
          res.redirect('/users/reset'); 
        }).catch(err => {
          console.log(err)
          return res.render('reset',{
				    errors: [{ msg: 'Something went wrong!' }],
            email
          })
        })
		} else {
			return res.render('reset', {
				errors: [{ msg: 'Email Not Registered' }],
        email
			});
		}
	});
});

router.post('/password-reset',(req,res) =>{
  const { email,password,password2 } = req.body
  console.log(email,password,password2)
  if(!password || !password2){
    return res.render('passwordReset',{
      email,
      password,
      password2,
      error_msg:"Password and Confirm password are required!"
    })
  }
  if(password !== password2){
    return res.render('passwordReset',{
      email,
      password,
      password2,
      error_msg:"Passwords doesn't match"
    })
  }
  if(password.length < 6){
    return res.render('passwordReset',{
      email,
      password,
      password2,
      error_msg:"Password must have minimum 6 characters"
    })
  }
  

  bcrypt.genSalt(10, (err, salt) => {
    bcrypt.hash(password, salt, async (err, hash) => {
      if (err) throw err;
      const user = await User.findOne({email})
      user.password = hash
      await user.save()
      req.flash(
        'success_msg',
        `Password Reset Successful`
      );
      return res.redirect('/users/login')
    })
  })
});

// Logout
router.get('/logout', (req, res) => {
	req.logout();
	req.flash('success_msg', 'You are logged out');
	res.redirect('/users/login');
});

module.exports = router;
