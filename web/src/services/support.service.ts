import { httpClient } from "@/lib/http-client";

export interface FeedbackData {
    category: string;
    message: string;
    rating: number;
}

export const supportService = {
    sendFeedback: async (data: FeedbackData): Promise<void> => {
        // Implementation once backend is ready
        // return httpClient.post('/feedback', data);

        console.log("Feedback sent:", data);
        return new Promise((resolve) => setTimeout(resolve, 1000));
    }
};
