
const {postCompletion} = require('./chat')
const { createBot, createProvider, createFlow, addKeyword, EVENTS } = require('@bot-whatsapp/bot')

const QRPortalWeb = require('@bot-whatsapp/portal')
const BaileysProvider = require('@bot-whatsapp/provider/baileys')
const MockAdapter = require('@bot-whatsapp/database/mock')


const flowPrincipal = addKeyword(EVENTS.WELCOME)
    .addAction(
        async (ctx,ctxFn) => {
            
            let messages = [
                { "role": "system", "content": "Eres ALEX, un modelo que corre de manera local, respondes mensajes de whatsapp de manera amistosa y simple en español." },
                { "role": "user", "content": ctx.body}
            ]
            const answer = await postCompletion(messages);
            console.log('Answer: ',answer);
            await ctxFn.flowDynamic(answer);
        }
    )
   
    
const main = async () => {
    const adapterDB = new MockAdapter()
    const adapterFlow = createFlow([flowPrincipal])
    const adapterProvider = createProvider(BaileysProvider)

    createBot({
        flow: adapterFlow,
        provider: adapterProvider,
        database: adapterDB,
    })

    QRPortalWeb()
}

main()

