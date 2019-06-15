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
    if(!this.req.me && !inputs.username) {
      return exits.success({
        id: 0,
        text: 'Para comenzar ingrese un correo electronico para identificarte como usuario y luego da click en comenzar'
      });
    }

    if(this.req.me.emailStatus == 'unconfirmed'){
      return exits.success({
        id: -2,
        text: 'Por favor confirme su correo electronico para comenzar a etiquetar, reconocer su identidad es muy útil para nosotros.'
      })
    }
    var record = undefined;
    var flat = false;

    var postUserTags = [];
    var username = this.req.me? this.req.me.emailAddress : inputs.username;
    if(username){
      var userTags = await Score.find({username: username}).select(['post']);
      userTags.forEach((i)=>{
        console.log(i.post);
        postUserTags.push(i.post)
      });

    }
    var max = await Post.count({id: { nin: postUserTags},complete:0}); //Post que no hallan superado la cantidad máxima de votaciones --> complete:0
    let skipRandom = Math.floor(Math.random()*max);
    record = await Post.find({id: { nin: postUserTags},complete:0}).skip(skipRandom).limit(1);

    record = record[0]; //Porque el record guarda el resultado de Post.find y no Post.findOne por lo que es un arreglo
    if (!record){
      record = {
        id: -1,
        text: 'No hay más publicaciones para este usuario, regresa más adelante para continuar colaborando. Muchas gracias por su interés.'
      };
    }
    return exits.success({
      id: record.id,
      text: record.text
    });

  }

};
