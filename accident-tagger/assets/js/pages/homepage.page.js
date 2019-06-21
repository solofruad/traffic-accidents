/*
  TODO:
   Antes el sistema permitía etiquetar para usuarios externos, ahora solo se permite únicamente usuarios logueados.
   Sin embargo no se cabmio nada del cóodigo, solo se cambio el valor del atribuo isLoggued a true, que antes se encontraba como false.
 */

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
    //Antes permitia que los usuarios no logueados pudieran etiquetar
      //isLogged: false,
    //Ahora solo los usuarios registrados pueden etiquetar
    isLogged: true,
    disableButton: false,
    isEmail: false,
    syncing: false,
    formErrors: {},
    cloudError: '',
    dashboardModalVisible: false,
    dashboardModalVisibleNegativo: false,
    imagesModal: {
      img1: '', img2: '', img3: '', img4: '', img5: '', img6: ''
    },
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
    this.post = await Cloud.getPost();
    this.uploadFormData.id = this.post.id;
    this.disableButton = this.post.id <= 0;
    if(this.me){
      this.uploadFormData.username = this.me.emailAddress;
      this.isEmail = true;
      this.isLogged = true;
      this.clickHeroButton();
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

    getPost: async function(){
      this.post = {};
      var style = "post-wrapper text-muted p-3 mb-5 bg-white rounded";
      this.$refs.textPost.className = "post-wrapper text-muted p-3 mb-5 bg-dark rounded";
      var fecth = await Cloud.getPost(this.uploadFormData.username);

      setTimeout(()=>{
        this.post = fecth;
        this.uploadFormData.id = this.post.id;
        this.$refs.textPost.className = style;
        this.disableButton = this.post.id <= 0;
        this.clickHeroButton();
      },100);
    },

    //Antes de mandar los datos al servidor
    handleParsingUploadTagForm: function(){
      // clear out any pre-existing error messages
      this.formErrors = {};
      var argins = this.uploadFormData;
      if(Object.keys(this.formErrors).length > 0){
        return;
      }
      return argins;
    },

    // Después de que los datos son enviados al servidor
    submittedUploadTagForm: async function(result){
      this.getPost();
    },

    setLabelFormData: function (event) {
      this.uploadFormData.label = event;
    },

    startLabeling: function () {
      if(this.validateEmail(this.uploadFormData.username)){
        this.disableButton = false;
        this.isEmail = true;
        this.getPost();
      }else{
        this.isEmail = false;
      }
    },

    validateEmail: function(email) {
      var re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return re.test(String(email).toLowerCase());
    },
    clickOpenDashboardModalButton: async function() {
      this.imagesModal.img1 = "/images/positivo/1.png";
      this.imagesModal.img2 = "/images/positivo/2.png";
      this.imagesModal.img3 = "/images/positivo/3.png";
      this.imagesModal.img4 = "/images/positivo/4.png";
      this.imagesModal.img5 = "/images/positivo/5.png";
      this.imagesModal.img6 = "/images/positivo/6.png";
      this.dashboardModalVisible = true;
    },

    closeDashboardModal: async function() {
      this.dashboardModalVisible = false;
      this.imagesModal.img1 = "";
      this.imagesModal.img2 = "";
      this.imagesModal.img3 = "";
      this.imagesModal.img4 = "";
      this.imagesModal.img5 = "";
      this.imagesModal.img6 = "";
    },

    clickOpenDashboardModalButtonNegativo: async function() {
      this.imagesModal.img1 = "/images/negativo/1.png";
      this.imagesModal.img2 = "/images/negativo/2.png";
      this.imagesModal.img3 = "/images/negativo/3.png";
      this.imagesModal.img4 = "/images/negativo/4.png";
      this.imagesModal.img5 = "/images/negativo/5.png";
      this.imagesModal.img6 = "/images/negativo/6.png";
      this.dashboardModalVisibleNegativo = true;
    },

    closeDashboardModalNegativo: async function() {
      this.dashboardModalVisibleNegativo = false;
      this.imagesModal.img1 = "";
      this.imagesModal.img2 = "";
      this.imagesModal.img3 = "";
      this.imagesModal.img4 = "";
      this.imagesModal.img5 = "";
      this.imagesModal.img6 = "";
    },



  }
});
