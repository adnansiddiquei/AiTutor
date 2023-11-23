spec = [
    {
        method: 'GET',
        endpoint: '/lessonSummary',
        params: {
            lessonId: 1
        },
        response: {
            summary: 'Lorem ipsum dolor sit amet...'
        }
    },

    {
        method: 'GET',
        endpoint: '/question',
        params: {
            lessonId: 1,
            questionNumber: 4
        },
        response: {
            id: '17',
            question: 'Which of the following is not a requirement of GIPS for composite construction?',
            answers: [
                'one or more portfolios.',
                'portfolios selected on an ex-post basis.',
                'portfolios managed according to a similar investment strategy.'
            ],
            correctAnswer: 0, // the position in the array which is the correct answer
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
            id: '17', // question id
            answer: 1,  // their answer
            timeTaken: 23  // in seconds
        }
    }
]