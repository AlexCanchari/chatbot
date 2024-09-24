const { postCompletion } = require('./chat'); 

const { createBot, createProvider, createFlow, addKeyword, EVENTS } = require('@builderbot/bot');

const { MemoryDB: Database } = require('@builderbot/bot');

const { BaileysProvider:provider } = require('@builderbot/provider-baileys')

const PORT = process.env.PORT ?? 3000

const mediaFlow  = addKeyword(EVENTS.MEDIA)
.addAnswer('Leyendo imagen....', { capture: false }, async (ctx, { provider }) => {
        const localPath = await provider.saveFile(ctx, {path:'./images'})
        ctx.localPath = localPath
})
.addAction(
    async (ctx, { flowDynamic }) => {
        const answer = await postCompletion(ctx.localPath);
        await flowDynamic(answer);
    }
)
   
    
const main = async () => {
    const adapterDB = new Database()
    const adapterFlow = createFlow([mediaFlow])
    const adapterProvider = createProvider(provider)

    const { httpServer }  = await createBot({
        flow: adapterFlow,
        provider: adapterProvider,
        database: adapterDB,
    })

    
    httpServer(+PORT)
    
}

main()

