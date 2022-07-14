# Installation
-------------------------------------------
* Clone this repository
* 
<table class="datatable" id="academictable">

                                      <thead>
                                        <th>#</th>
                                        <th>Code</th>
                                        <th>Subject</th>
                                        <th>Assignment 1</th>
                                        <th>Assignment 2</th>
                                        <th>Series 1</th>
                                        <th>Series 2</th>
                                        <th>Attendance(%)</th>
                                        <th>Total Mark</th>
                                        <th>University Result</th>
                                        <th>No.of Chances</th>
                                        <th>Credit</th>

                                      </thead>


                                        <tbody>
                                          {% for j in assign_subject_data %}
                                  {% if  j.semester == 1 %}
                                  <tr>


                                    <td>{{ forloop.counter }}</td>
                                    {% for i in subject_data %}
                                    {% if j.subject_id == i.id %}

                                    <td>{{i.code}}</td>
                                    <td>{{i.subject_name}}</td>



                                    <td>
                                      {% for k in internal_mark_data %}
                                    {% if k.semester == 1 %}
                                    {% if k.subject_id == i.id %}
                                      {% if k.exam_type == 'Assignment 1' %}
                                        {{k.mark}}

                                      {% endif %}
                                      {% endif %}
                                      {% endif %}
                                      {% endfor %}
                                    </td>


                                    <td>{% for k in internal_mark_data %}
                                    {% if k.semester == 1 %}
                                    {% if k.subject_id == i.id %}

                                    {% if k.exam_type == 'Assignment 2' %}
                                        {{k.mark}}

                                      {% endif %}
                                    {% endif %}
                                    {% endif %}
                                    {% endfor %}</td>

                                    <td>{% for k in internal_mark_data %}
                                      {% if k.semester == 1 %}
                                      {% if k.subject_id == i.id %}

                                      {% if k.exam_type == 'Internal 1' %}
                                          {{k.mark}}

                                        {% endif %}
                                      {% endif %}
                                      {% endif %}
                                      {% endfor %}</td>

                                   <td>{% for k in internal_mark_data %}
                                    {% if k.semester == 1 %}
                                    {% if k.subject_id == i.id %}

                                    {% if k.exam_type == 'Internal 2' %}
                                        {{k.mark}}

                                      {% endif %}
                                    {% endif %}
                                    {% endif %}
                                    {% endfor %}</td>
                                    <td>
                                      {% for att in attendance_list %}
                                      {% if att.2 == 1 %}
                                      {% if att.0 == i.id %}
                                        {{att.3}} %
                                      {% endif %}
                                      {% endif %}
                                      {% endfor %}
                                    </td>
                                    <td>
                                    {% for w in total_mark_list %}
                                      {% if j.subject_id == w.0 %}
                                        {{w.3}}

                                      {% endif %}
                                    {% endfor %}
                                    </td>

                                    <td>{% for k in sem_result_list %}
                                      {% if k.0 == j.subject_id %}

                                      {% if k.3 == 10 %}
                                            O
                                          {% elif k.3 == 9 %}
                                            A+
                                          {% elif k.3 == 8.5 %}
                                            A
                                          {% elif k.3 == 8 %}
                                            B+
                                          {% elif k.3 == 7 %}
                                            B
                                          {% elif k.3 == 6 %}
                                            C
                                          {% elif k.3 == 5 %}
                                            P
                                          {% elif k.3 < 5 %}
                                            F
                                          {% endif %}
                                      {% endif %}
                                      {% endfor %}</td>
                                    <td>{% for k in sem_result_list %}
                                      {% if k.0 == j.subject_id %}
                                      {{k.4}}
                                      {% endif %}
                                      {% endfor %}</td>



                                    <td>{{i.credit}}</td>
                                    {% endif %}
                                    {% endfor %}

                                  </tr>
                                  {% endif %}
                              {% endfor %}




                                        </tbody>



                                  </table><table class="datatable" id="academictable">

                                      <thead>
                                        <th>#</th>
                                        <th>Code</th>
                                        <th>Subject</th>
                                        <th>Assignment 1</th>
                                        <th>Assignment 2</th>
                                        <th>Series 1</th>
                                        <th>Series 2</th>
                                        <th>Attendance(%)</th>
                                        <th>Total Mark</th>
                                        <th>University Result</th>
                                        <th>No.of Chances</th>
                                        <th>Credit</th>

                                      </thead>


                                        <tbody>
                                          {% for j in assign_subject_data %}
                                  {% if  j.semester == 1 %}
                                  <tr>


                                    <td>{{ forloop.counter }}</td>
                                    {% for i in subject_data %}
                                    {% if j.subject_id == i.id %}

                                    <td>{{i.code}}</td>
                                    <td>{{i.subject_name}}</td>



                                    <td>
                                      {% for k in internal_mark_data %}
                                    {% if k.semester == 1 %}
                                    {% if k.subject_id == i.id %}
                                      {% if k.exam_type == 'Assignment 1' %}
                                        {{k.mark}}

                                      {% endif %}
                                      {% endif %}
                                      {% endif %}
                                      {% endfor %}
                                    </td>


                                    <td>{% for k in internal_mark_data %}
                                    {% if k.semester == 1 %}
                                    {% if k.subject_id == i.id %}

                                    {% if k.exam_type == 'Assignment 2' %}
                                        {{k.mark}}

                                      {% endif %}
                                    {% endif %}
                                    {% endif %}
                                    {% endfor %}</td>

                                    <td>{% for k in internal_mark_data %}
                                      {% if k.semester == 1 %}
                                      {% if k.subject_id == i.id %}

                                      {% if k.exam_type == 'Internal 1' %}
                                          {{k.mark}}

                                        {% endif %}
                                      {% endif %}
                                      {% endif %}
                                      {% endfor %}</td>

                                   <td>{% for k in internal_mark_data %}
                                    {% if k.semester == 1 %}
                                    {% if k.subject_id == i.id %}

                                    {% if k.exam_type == 'Internal 2' %}
                                        {{k.mark}}

                                      {% endif %}
                                    {% endif %}
                                    {% endif %}
                                    {% endfor %}</td>
                                    <td>
                                      {% for att in attendance_list %}
                                      {% if att.2 == 1 %}
                                      {% if att.0 == i.id %}
                                        {{att.3}} %
                                      {% endif %}
                                      {% endif %}
                                      {% endfor %}
                                    </td>
                                    <td>
                                    {% for w in total_mark_list %}
                                      {% if j.subject_id == w.0 %}
                                        {{w.3}}

                                      {% endif %}
                                    {% endfor %}
                                    </td>

                                    <td>{% for k in sem_result_list %}
                                      {% if k.0 == j.subject_id %}

                                      {% if k.3 == 10 %}
                                            O
                                          {% elif k.3 == 9 %}
                                            A+
                                          {% elif k.3 == 8.5 %}
                                            A
                                          {% elif k.3 == 8 %}
                                            B+
                                          {% elif k.3 == 7 %}
                                            B
                                          {% elif k.3 == 6 %}
                                            C
                                          {% elif k.3 == 5 %}
                                            P
                                          {% elif k.3 < 5 %}
                                            F
                                          {% endif %}
                                      {% endif %}
                                      {% endfor %}</td>
                                    <td>{% for k in sem_result_list %}
                                      {% if k.0 == j.subject_id %}
                                      {{k.4}}
                                      {% endif %}
                                      {% endfor %}</td>



                                    <td>{{i.credit}}</td>
                                    {% endif %}
                                    {% endfor %}

                                  </tr>
                                  {% endif %}
                              {% endfor %}




                                        </tbody>



                                  </table>