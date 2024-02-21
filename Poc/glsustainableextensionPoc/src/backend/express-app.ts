import * as express from 'express';
import { Request, Response } from 'express';
import * as jsonServer from 'json-server';
import axios from 'axios';
import * as cors from 'cors';

const app = express();
app.use(cors());

const jsonServerMiddleware = jsonServer.router('db.json');
app.use('/api', jsonServerMiddleware);

// Additional route for handling GET /posts using axios
app.get('/posts', async (req: Request, res: Response) => {
  try {
    // Use axios to make the GET request
    const axiosResponse = await axios.get('http://localhost:3000/api/posts');

    // Assuming json-server returns data in axiosResponse.data
    res.json(axiosResponse.data);
  } catch (error: any) {
    // Handle errors gracefully
    console.error('Error fetching data:', error.message);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

// Start the server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
