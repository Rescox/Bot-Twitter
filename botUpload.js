console.log("Proceso de subir fotos");

var Twit = require('twit');
var fs = require('fs');
var dir = './Imagenes';

var T = new Twit({
    consumer_key:         'FCVYt7lC1jlFTt8s0HxU0K4g3',
    consumer_secret:      'Tt2MUUSMd9hP75AMUqWLziqrNRngjWB9y4Na7HhhuZRD3d2ibI',
    access_token:         '1063814327587799041-6rmZ9wMrhMD5cWcSAd0ANMgsV2ZPGl',
    access_token_secret:  'b8sxtICZo2D3XyTE5KrQx0Y9soVRrfXnWg81fuGG9nSVa',
    timeout_ms:           60*1000,  // optional HTTP request timeout to apply to all requests.
    strictSSL:            true,     // optional - requires SSL certificates to be valid.
  })
var i = 14;
//tweetIt();
setInterval(tweetIt, 1000*3);


function tweetIt(){
    var n = fs.readdir(dir, (err, files) => {
        var n = files.length
        console.log(n);
        return n;
    }); 
    if(i === n)
        i = 1;
    var filename = 'Imagenes/P' + i +'.jpeg';
    var params = {
        encoding: 'base64'
    }
    console.log("asdasdas");
    if(fs.existsSync(filename)) { 
        var b64 = fs.readFileSync(filename, params);
        T.post('media/upload', { media_data: b64 }, uploaded);
    }
    function uploaded(err, data, response){
        var id = data.media_id_string;
        var tweet = {
            status: i + ' - Puzzle del Profesor Layton y la Villa Misteriosa',
            media_ids: [id]
        }
        T.post('statuses/update', tweet, tweeted);
    }

    function tweeted(err, data, reponse) {
        if (err) 
            console.log("Algo fue mal");
        else
            console.log("Ha funcionado");
        i++;
    }  
}

