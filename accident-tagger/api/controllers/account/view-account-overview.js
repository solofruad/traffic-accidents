module.exports = {


  friendlyName: 'View account overview',


  description: 'Display "Account Overview" page.',


  exits: {

    success: {
      viewTemplatePath: 'pages/account/account-overview',
    }

  },


  fn: async function (inputs, exits) {

    // If billing features are enabled, include our configured Stripe.js
    // public key in the view locals.  Otherwise, leave it as undefined.
    progress = this.req.me ? await Score.count({username: this.req.me.emailAddress}) : 0;
    return exits.success({
      stripePublishableKey: sails.config.custom.enableBillingFeatures? sails.config.custom.stripePublishableKey : undefined,
      progress: progress,
    });

  }


};
