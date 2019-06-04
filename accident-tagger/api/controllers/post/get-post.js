module.exports = {


  friendlyName: 'Get post',


  description: 'Mostrar un tweet para ser clasificado',


  inputs: {
    username:{
      type: 'string',
      description: 'Para no traer las publicaciones que este usuario ya halla clasificado',
    }
  },


  exits: {
    success:{
      statusCode:200,
      outputDescription: 'Tweet para calificar generado',
      outputType:{
        id: 'number',
        text: 'string'
      }
    },
    badRequest: {
      description: 'No se pudo obtener un tweet',
      responseType: 'badRequest'
    }
  },


  fn: async function (inputs, exits) {
    //var max = await Post.find({sort:'id DESC',limit:1, select: ['id'] });
    //TODO: ya se puede descartar las publicaciones que el usuario registrado ya clasificó,pero falta hacer lo mismo para el ususario que no esta registrado y agrega su email
    // en el input de homepage.ejs
    console.log(inputs.username);
    var record = undefined;
    var flat = false;

    //while (flat === false){
      //let idRandom = Math.floor(Math.random()*max[0].id)+1;

      //TODO: Falta traer un post que este por debajo de cierta cantidad de votaciones en la tabla Score
      //record = await Post.find({complete:0}).skip(skipRandom).populate('post_score');
      var postUserTags = [];
      if(this.req.me){
        var userTags = await Score.find({username: this.req.me.emailAddress}).select(['post']);
        userTags.forEach((i)=>{
          console.log(i.post);
          postUserTags.push(i.post)
        });
        //console.log(Object.values(userTags[0]));
        console.log(typeof Object.values(postUserTags));

      }
      var max = await Post.count({id: { nin: postUserTags},complete:0});
      let skipRandom = Math.floor(Math.random()*max);
      record = await Post.find({id: { nin: postUserTags},complete:0}).skip(skipRandom).limit(1);
      //record = await Post.find({complete:0}).skip(skipRandom).limit(1);
      //if(record[0].post_score.length < 3){
      // if(record !== undefined){
        //scoreCount = await Score.count({post:record.id});
        //console.log(scoreCount);
        //TODO: si ya no hay tweets por calificar esto se repite infinitamente
        //if(scoreCount <= 2) flat = true;
        //console.log(record.post_score.length);
        //if(record[0].post_score.length < 3)
        //  flat = true;
      //}
    //}

    /*var score = await Score.find({id:17}).populate('post');
    console.log(score);*/
    record = record[0];
    if (!record){
      record = {
        id: -1,
        text: 'No hay más publicaciones para clasificar. Muchas gracias'
      };
    }
    return exits.success({
      id: record.id,
      text: record.text
    });

  }


};
