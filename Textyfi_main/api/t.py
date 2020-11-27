def getPredictions():
    import pickle
    review="your product is bad"
    model = pickle.load(open("model.sav", "rb"))
    scaled = pickle.load(open("scaler.sav", "rb"))
    prediction = model.predict(scaled.transform([review]))
    print(prediction[0])
    # if prediction == 0:
    #     return "not survived"
    # elif prediction == 1:
    #     return "survived"
    # else:
    #     return "error"
        
    # return render(request, 'result.html', {'result':predi})
# our result page view
# def result(request):
#     pclass = int(request.GET['pclass'])
#     sex = int(request.GET['sex'])
#     age = int(request.GET['age'])
#     sibsp = int(request.GET['sibsp'])
#     parch = int(request.GET['parch'])
#     fare = int(request.GET['fare'])
#     embC = int(request.GET['embC'])
#     embQ = int(request.GET['embQ'])
#     embS = int(request.GET['embS'])

#     result = getPredictions(pclass, sex, age, sibsp, parch, fare, embC, embQ, embS)

getPredictions()