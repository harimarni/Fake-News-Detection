const express = require('express');
const router = express.Router();
const { ensureAuthenticated, forwardAuthenticated } = require('../config/auth');
const User = require('../models/User');
var jwt = require('jsonwebtoken');

// Welcome Page
router.get('/', forwardAuthenticated, (req, res) => res.render('welcome'));

//validate token
router.get('/validate/:token', (req, res) => {
	const { token } = req.params;
	var decoded = jwt.verify(token, process.env.JWT_SECRET);
	const { name, email, password } = decoded;
	if (decoded && password && name && email) {
		User.findOne({ email: email }).then((user) => {
			console.log(user)
			if (!user) {
				const newUser = new User({
					name,
					email,
					password,
				});
				newUser
					.save()
					.then((data) => {
						req.flash('success_msg', 'Email verified Successfully!!');
						res.redirect('/users/login');
					})
					.catch((err) => {
						req.flash('error_msg', 'Cannot create account!');
						res.redirect('/users/login');
					});
			} else {
				req.flash('error_msg', 'Email Already Verified');
				res.redirect('/users/login');
			}
		});
	} else {
		req.flash('error_msg', 'Email verfication failed!');
		res.redirect('/users/login');
	}
});

//reset Password
router.get('/reset/:token', (req, res) => {
	const { token } = req.params;
	var decoded = jwt.verify(token, process.env.JWT_SECRET);
	const { email } = decoded;
	if (!email) {
    return res.render('passwordReset',{
      error_msg:"Invalid Email for Password Reset!"
    })
	}
  res.render('passwordReset',{
    email,
    success_msg:"Enter your New password Below"
  })
});

// Dashboard
router.get('/dashboard', ensureAuthenticated, (req, res) =>
	res.render('dashboard', {
		user: req.user,
	})
);

module.exports = router;
