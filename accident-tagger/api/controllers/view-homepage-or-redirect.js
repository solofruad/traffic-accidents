module.exports = {


  friendlyName: 'View homepage or redirect',


  description: 'Display or redirect to the appropriate homepage, depending on login status.',


  exits: {

    success: {
      statusCode: 200,
      description: 'Requesting user is a guest, so show the public landing page.',
      viewTemplatePath: 'pages/homepage'
    },

    redirect: {
      responseType: 'redirect',
      description: 'Requesting user is logged in, so redirect to the internal welcome page.'
    },

  },


  fn: async function (inputs, exits) {

    /*if (this.req.me) {
      throw {redirect:'/welcome'};
    }*/

    /*var max = await Post.find({sort:'id DESC',limit:1, select: ['id'] });
    var record = undefined;
    var flat = false;

    while (flat === false){
      let idRandom = Math.floor(Math.random()*max[0].id)+1;
      console.log("idRandom: "+idRandom)
      //TODO: Falta traer un post que este por debajo de cierta cantidad de votaciones en la tabla Score
      record = await Post.findOne({id: idRandom});

      if(record !== undefined){
        flat = true;
      }
    }
    console.log("id: "+record.id);*/
    //var record = await Cloud.getPost();
    return exits.success();
  }


};
