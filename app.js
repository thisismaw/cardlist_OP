const express = require('express');
const { MongoClient } = require('mongodb');

const app = express();
const PORT = process.env.PORT || 3000;

// MongoDB Atlas connection URI
const atlasConnectionUri = "mongodb+srv://admin:8883mb@onepiece.c2dddqy.mongodb.net/?retryWrites=true&w=majority";
const client = new MongoClient(atlasConnectionUri);

// Connect to MongoDB Atlas
async function connectToMongoDB() {
    try {
        await client.connect();
        console.log("Connected to MongoDB");
    } catch (e) {
        console.error(e);
    }
}

connectToMongoDB();

// Serve static files from 'public' directory
app.use(express.static('public'));

// Root route
app.get('/', (req, res) => {
    res.send('Welcome to the OPVault Server!');
});

// Endpoint to serve card data from MongoDB
app.get('/data', async (req, res) => {
    try {
        const collection = client.db('OnePiece').collection('OPdb');
        const data = await collection.find({}).toArray();
        res.json(data);
    } catch (e) {
        res.status(500).send(e.toString());
    }
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
