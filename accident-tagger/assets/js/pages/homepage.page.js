parasails.registerPage('homepage', {
  //  ╦╔╗╔╦╔╦╗╦╔═╗╦    ╔═╗╔╦╗╔═╗╔╦╗╔═╗
  //  ║║║║║ ║ ║╠═╣║    ╚═╗ ║ ╠═╣ ║ ║╣
  //  ╩╝╚╝╩ ╩ ╩╩ ╩╩═╝  ╚═╝ ╩ ╩ ╩ ╩ ╚═╝
  data: {
    heroHeightSet: false,
    post: {
      id: '',
      text: ''
    },
    uploadFormData: {
      label: '',
      username: '',
      id: '',
    },
    isLogged: false,
    syncing: false,
    formErrors: {},
    cloudError: '',
  },

  //  ╦  ╦╔═╗╔═╗╔═╗╦ ╦╔═╗╦  ╔═╗
  //  ║  ║╠╣ ║╣ ║  ╚╦╝║  ║  ║╣
  //  ╩═╝╩╚  ╚═╝╚═╝ ╩ ╚═╝╩═╝╚═╝
  beforeMount: function() {
    // Attach any initial data from the server.
    _.extend(this, SAILS_LOCALS);
    //this.post = {id: 1212, text: 'ccc'};

  },
  mounted: async function(){
    this._setHeroHeight();
    this.post = await Cloud.getPost('');
    this.uploadFormData.id = this.post.id;
    if(this.me){
      this.uploadFormData.username = this.me.emailAddress;
      this.isLogged = true;
    }
  },

  //  ╦╔╗╔╔╦╗╔═╗╦═╗╔═╗╔═╗╔╦╗╦╔═╗╔╗╔╔═╗
  //  ║║║║ ║ ║╣ ╠╦╝╠═╣║   ║ ║║ ║║║║╚═╗
  //  ╩╝╚╝ ╩ ╚═╝╩╚═╩ ╩╚═╝ ╩ ╩╚═╝╝╚╝╚═╝
  methods: {

    clickHeroButton: async function() {
      // Scroll to the 'get started' section:
      $('html, body').animate({
        scrollTop: this.$find('[role="scroll-destination"]').offset().top
      }, 500);
    },

    // Private methods not tied to a particular DOM event are prefixed with _
    _setHeroHeight: function() {
      var $hero = this.$find('[full-page-hero]');
      var headerHeight = $('#page-header').outerHeight();
      var heightToSet = $(window).height();
      heightToSet = Math.max(heightToSet, 500);//« ensure min height of 500px - header height
      heightToSet = Math.min(heightToSet, 1000);//« ensure max height of 1000px - header height
      $hero.css('min-height', heightToSet - headerHeight+'px');
      this.heroHeightSet = true;
    },

    handleParsingUploadTagForm: function(){
      // clear out any pre-existing error messages
      this.formErrors = {};
      var argins = this.uploadFormData;
      if(Object.keys(this.formErrors).length > 0){
        return;
      }
      return argins;
    },


    submittedUploadTagForm: async function(result){
      this.post = {};
      var style = "post-wrapper text-muted p-3 mb-5 bg-white rounded";
      this.$refs.textPost.className = "post-wrapper text-muted p-3 mb-5 bg-dark rounded";
      var fecth = await Cloud.getPost(this.uploadFormData.username);
      setTimeout(()=>{
        this.post = fecth;
        this.uploadFormData.id = this.post.id;
        this.$refs.textPost.className = style;
      },100);


    },

    setLabelFormData: function (event) {
      this.uploadFormData.label = event;
    }

  }
});
