from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def handle_selection():
    if request.method == 'GET':
        return render_template('student_form.html')  # Display form on GET request
    elif request.method == 'POST':
        selection = request.form['ID']  # Access selection using correct key
        selection_val = request.form.get('id_value')  # Get ID value using get() for potential missing key
        if selection:  # Check if selection exists before branching
            if selection == 'student_id':
                student = get_details_from_csv(selection_val, 'student')
                # return student
                return render_template('student_score.html', students=student)
            elif selection == 'course_id':
                course_data = {'course_name': 'Programming 101', 'average_score': 85}
                return render_template('course_score.html', course_data=course_data)
            else:
                # Handle invalid selection (optional)
                return render_template('error.html', message="Invalid selection")
        else:
            # Handle case where user doesn't select anything (optional)
            return render_template('student_form.html', message="Please select an option")

def get_details_from_csv(id, type):
    with open('data.csv', 'r') as f:
        data = []
        score_record = []
        for line in f:
            if str(id) in line:
                data.append(line.rstrip('\n'))

        if type == 'student':
            score = 0
            for line in data:
                sub_score = []
                score += int(line.split(',')[2])
                sub_score.append(id)
                sub_score.append(line.split(',')[1])
                sub_score.append(line.split(',')[2])
                score_record.append(sub_score)
            return [score, score_record]

        elif type == 'course':
            max_score = 0
            average_score = 0
            total_score = 0
            count = 0  # Corrected initialization to 0

            for line in data:
                values = line.split(',')
                score = int(values[2])  # Use split and access by index
                score_record.append(score)
                total_score += score
                count += 1
                if score > max_score:
                    max_score = score
            average_score = total_score / count  # Corrected division by count

            return [max_score, average_score, data, score_record]

if __name__ == '__main__':
    app.debug = True
    app.run()
