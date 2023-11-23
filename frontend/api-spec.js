spec = [
    {
        method: 'GET',
        endpoint: '/lessonSummary',
        response: {
            summary: 'Lorem ipsum dolor sit amet...'
        }
    },

    {
        method: 'GET',
        endpoint: '/question',
        response: {
            id: 'ae9b82d3-6c90-483f-897c-936fb86b42bb',
            question: 'Which of the following is not a requirement of GIPS for composite construction?',
            answers: [
                'one or more portfolios.',
                'portfolios selected on an ex-post basis.',
                'portfolios managed according to a similar investment strategy.'
            ],
            correctAnswer: 0 // the position in the array which is the correct answer
            lessonFinished: false
        }
    },
    { // when the lesson is finished
        method: 'GET',
        endpoint: '/question',
        response: {
            lessonFinished: true
        }
    },


    {
        method: 'POST',
        endpoint: '/question',
        data: {
            id: 'ae9b82d3-6c90-483f-897c-936fb86b42bb', // question id
            answer: 1,
            timeTaken: 23  // in seconds
        }
    }
]