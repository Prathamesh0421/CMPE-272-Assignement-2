import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentRecords')

def lambda_handler(event, context):
    try:
        http_method = event['httpMethod']

        # POST -Create a new student record
        if http_method == 'POST':
            student = json.loads(event['body'])
            table.put_item(Item=student)
            return {
                'statusCode': 200,
                'body': json.dumps('Student record added successfully')
            }

        # GET -  Fetch an existing student record
        elif http_method == 'GET':
            student_id = event['queryStringParameters']['student_id']
            response = table.get_item(Key={'student_id': student_id})
        
            if 'Item' in response:
                item = response['Item']
                ordered_item = {
                    'student_id': item['student_id'],
                    'name': item['name'],
                    'age': item['age'],
                    'course': item['course']
                }
                return {
                    'statusCode': 200,
                    'body': json.dumps(ordered_item)
                }
            else:
                return {
                    'statusCode': 404,
                    'body': json.dumps({'error': 'Student record not found'})
                }


        # PUT- Update an existing student record 
        elif http_method == 'PUT':
            student_id = event['queryStringParameters']['student_id']
            student = json.loads(event['body'])
            table.update_item(
                Key={'student_id': student_id},
                UpdateExpression='SET #name = :name, #age = :age, #course = :course',
                ExpressionAttributeNames={
                    '#name': 'name',
                    '#age': 'age',
                    '#course': 'course'
                },
                ExpressionAttributeValues={
                    ':name': student['name'],
                    ':age': student['age'],
                    ':course': student['course']
                }
            )
            return {
                'statusCode': 200,
                'body': json.dumps('Student record updated successfully')
            }

        # DELETE -  Remove an existing student record
        elif http_method == 'DELETE':
            student_id = event['queryStringParameters']['student_id']
            table.delete_item(Key={'student_id': student_id})
            return {
                'statusCode': 200,
                'body': json.dumps('Student record deleted successfully')
            }

      
        else:
            return {
                'statusCode': 405,
                'body': json.dumps({'error': f'Method {http_method} not allowed'})
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
