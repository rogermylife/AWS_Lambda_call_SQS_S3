import boto3
import uuid
import os
import urllib



SQS = boto3.resource('sqs')
INPUTQ = SQS.Queue('https://sqs.us-east-1.amazonaws.com/005368682193/input')
OUTPUTQ = SQS.Queue('https://sqs.us-east-1.amazonaws.com/005368682193/output')

BUCKET_NAME = 'nthu105062548'
S3 = boto3.resource('s3')



# print(response.get('MessageId'))
# print(response.get('MD5OfMessageBody'))

def lambda_handler(event, context):
    for message in INPUTQ.receive_messages():
        # Get the custom author message attribute if it was set
        # Print out the body and author (if set)
        # print 'Hello, {0}!'.format(context.aws_request_id)
        print 'Hello, {0}!'.format('context.aws_request_id')
        job_id = str(uuid.uuid4())
        download_url = process_message(message.body, job_id)

        response = OUTPUTQ.send_message(MessageBody=download_url)
        print response
        # Let the queue know that the message is processed
        message.delete()

    print "[LAMBDA END]"


def process_message(message, job_id):
    print "process start"
    try:
        output_dir = "/tmp/"
		# Download images from URLs specified in message
        for line in message.splitlines():
            print "Downloading image from %s" % line
            # res = os.system("wget -P %s %s" % (output_dir, line))
            urllib.urlretrieve(line, '/tmp/'+str(uuid.uuid4())+'.jpg')
            # os.system("wget -OutFile %s.jpg %s" % (output_dir, line))
        output_image_name = "output-%s.jpg" % (job_id)
        output_image_path = output_dir + output_image_name
        listdir()
		# Invoke ImageMagick to create a montage
        print 'montage '+output_image_name
        os.system("montage -size 400x400 null: %s*.* null: -thumbnail 400x400 -bordercolor white -background black +polaroid -resize 80%% -gravity center -background black -geometry -10+2  -tile x1 %s" % (output_dir, output_image_path))
        print 'montage done'
        listdir()
        print 'upload file '+output_image_path
        S3.Object(BUCKET_NAME, output_image_name).put(Body=open(output_image_path, 'rb'))
        print 'upload done'
        download_url = "https://s3.amazonaws.com/%s/%s" % (BUCKET_NAME, output_image_name)
        return download_url

        # Write the resulting image to s3
		#output_url = write_image_to_s3(output_image_path, output_image_name, s3_output_bucket, s3_endpoint)

		# Return the output url
		#return output_url
    except:
        print "ERRORRRRRRRRRRRRRRRR"

def listdir():
    print 'show /tmp/'
    for filename in os.listdir("/tmp/"):
        print  filename

def insert_data():
    input_messege = ("https://us-east-1-aws-training.s3.amazonaws.com/arch-static-assets/static/20120728-DSC01265-L.jpg\n"
                    "https://us-east-1-aws-training.s3.amazonaws.com/arch-static-assets/static/20120728-DSC01267-L.jpg\n"
                    "https://us-east-1-aws-training.s3.amazonaws.com/arch-static-assets/static/20120728-DSC01292-L.jpg\n"
                    "https://us-east-1-aws-training.s3.amazonaws.com/arch-static-assets/static/20120728-DSC01315-L.jpg\n"
                    "https://us-east-1-aws-training.s3.amazonaws.com/arch-static-assets/static/20120728-DSC01337-L.jpg\n")
    INPUTQ.send_message(MessageBody=input_messege)



if __name__ == '__main__':
    insert_data()
    lambda_handler("XD", "XD")

