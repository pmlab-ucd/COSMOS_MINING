from sklearn_porter import Porter
from sklearn_utils import SklearnUtils

def model2java(clf):
    # Transpile classifier:
    result = Porter(language='java').port(clf)
    print(result)

    out_dir = SklearnUtils.out_dir

    java_file = open(out_dir + 'RandomForestModel.java', 'w')
    for line in result:
        line = str(line).replace('Tmp', 'RandomForestModel')
        java_file.write(line)